from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render
from apps.core.models import (Server, UsageLog, CpuUsage, MemoryUsage,
                         DiskUsage, ProcessUsage, NetworkUsage, ErrorLog,
                         BackupTarget, BackupLog)
import json
from django.utils import timezone
import datetime

# /api/update
def update(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    try:
        data = json.loads(request.body)
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
