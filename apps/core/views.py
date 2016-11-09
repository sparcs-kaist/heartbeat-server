from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.core.models import Server
from apps.core.sparcsssov2 import Client
import random
import json


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
        return HttpResponseBadRequest()

    if 'server' not in data or \
            'name' not in data['server'] or 'key' not in data['server']:
        return HttpResponseBadRequest()

    server_name = data['server']['name']
    server_key = data['server']['key']

    servers = Server.objects.filter(name=server_name)
    if len(servers) == 0:
        return HttpResponseNotFound()

    server = servers[0]
    if server.key != server_key:
        return HttpReponseForbidden()

    # update here

    return JsonResponse({'success': True})
