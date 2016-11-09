from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from apps.core.models import (Server, UsageLog, CpuUsage, MemoryUsage,
                         DiskUsage, ProcessUsage, NetworkUsage, ErrorLog,
                         BackupTarget, BackupLog)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from apps.core.models import Server
from apps.core.sparcsssov2 import Client
import random
import json
import datetime

sso_client = Client(settings.SSO_ID, settings.SSO_KEY)


# /
def main(request):
    return render(request, 'main.html')


# /login/
def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    login_url, state = sso_client.get_login_params()
    request.session['state'] = state
    return redirect(login_url)


# /login/callback/
def login_callback(request):
    state_before = request.session.get('state', '')
    state = request.GET.get('state', '')
    if state_before != state:
        return HttpResponseBadRequest()

    code = request.GET.get('code', '')
    profile = sso_client.get_user_info(code)

    sparcs_id = profile['sparcs_id']
    if not sparcs_id:
        return HttpResponseForbidden()

    user_list = User.objects.filter(first_name=sparcs_id)
    if len(user_list) == 0:
        user = User.objects.create_user(username=profile['sid'],
                                        email=profile['email'],
                                        password=str(random.getrandbits(32)),
                                        first_name=profile['sparcs_id'],
                                        last_name='')
        user.save()
    else:
        user = user_list[0]

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    return redirect('/')



# /logout/
def logout(request):
    if not request.user.is_authenticated():
        return redirect('/')

    sid = request.user.username
    logout_url = sso_client.get_logout_url(sid, '/')

    auth.logout(request)
    return redirect(logout_url)


# /unregister/
def unregister(request):
    return HttpResponse('<script>alert("You cannot unregister SPARCS Heartbeat."); window.history.back();</script>')


# /api/update
@csrf_exempt
def update(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed('POST')

    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        print('parse failed')
        return HttpResponseBadRequest()

    if 'server' not in data or \
            'name' not in data['server'] or 'key' not in data['server']:
        return HttpResponseBadRequest()

    server_name = data['server']['name']
    server_key = data['server']['key']

    print('find server')
    servers = Server.objects.filter(name=server_name)
    if len(servers) == 0:
        return HttpResponseNotFound()

    server = servers[0]
    if server.key != server_key:
        return HttpReponseForbidden()
    
    # update here
    print("now update!!!!!!!!!!!")
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    server.ip = ip
    server.save()
    
    info = data['info']
    usage = UsageLog.objects.create(server=server, datetime=timezone.now())
    usage.save()
    cpu = CpuUsage.objects.create(usagelog=usage, user=info['cpu']['user'],
                                  system=info['cpu']['system'], idle=info['cpu']['system'])
    cpu.save()
    for k, v in info['disk'].items():
        disk = DiskUsage.objects.create(usagelog=usage, device_name=k, fs_type=v['fs_type'],
                                        mount_point=v['mount_point'],
                                        used=v['used'], total=v['total'])
        disk.save()
        
    mem_info = info['mem']
    mem = MemoryUsage.objects.create(usagelog=usage, swap_total=mem_info['swap']['total'],
                                     swap_used=mem_info['swap']['used'],
                                     virt_avail=mem_info['virtual']['avail'],
                                     virt_used=mem_info['virtual']['used'],
                                     virt_total=mem_info['virtual']['total'])
    mem.save()

    proc_info = info['proc']
    for i, p in enumerate(proc_info['top_cpu']):
        proc_cpu = ProcessUsage.objects.create(usagelog=usage, type='C', name=p['name'],
                                               order=i+1, cpu=p['cpu'], memory=p['mem'])
        proc_cpu.save()
    for i, p in enumerate(proc_info['top_mem']):
        proc_mem = ProcessUsage.objects.create(usagelog=usage, type='M', name=p['name'],
                                               order=i+1, cpu=p['cpu'], memory=p['mem'])
        proc_mem.save()

    net = NetworkUsage.objects.create(usagelog=usage, bytes_recv=info['net']['bytes_recv'],
                                      bytes_sent=info['net']['bytes_sent'],
                                      packet_recv=info['net']['packets_recv'],
                                      packet_sent=info['net']['packets_sent'])
    net.save()

    for k, v in data['errors'].items():
        try:
            error = ErrorLog.objects.create(usagelog=usage,
                                        datetime=timezone.make_aware(datetime.datetime.fromtimestamp(
                                            int(k))), log=v)
            error.save()
        except:
            continue
        
    return JsonResponse({'success': True})
