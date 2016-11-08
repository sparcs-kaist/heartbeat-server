from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render
from core.models import Server


# /api/update
def update(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    try:
        data = json.loads(request.body)
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
