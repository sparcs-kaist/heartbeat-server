from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.core.models import Server
import json


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
