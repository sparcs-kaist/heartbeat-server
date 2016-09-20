# Heartbeat Client for SPARCS Services
# Version 0.0.1 - 2016-09-18


import json
import psutil
import time
import requests


SERVICE_NAME = ''
SERVICE_KEY = ''
API_ENDPOINT = 'https://'


# get cpu info
# - user, system, idle (3 sec)
def get_cpu():
    pass


# get memory info
# - virtual (total, available, used)
# - swap (total, used)
def get_mem():
    pass


# get disk info
# - devide (mountpoint, fstype, total, used)
def get_disk():
    pass


# get network info
# - bytes (sent, recv) (3 sec)
# - packet (sent, recv) (3 sec)
def get_net():
    pass


# get process info
# - name (top 5 cpu usages)
# - name (top 5 mem usages)
def get_proc():
    pass


# get system info
# - boot time
def get_sys():
    pass


# our main routine
def main():
    info = {
        'cpu': get_cpu(),
        'mem': get_mem(),
        'disk': get_disk(),
        'net': get_net(),
        'proc': get_proc(),
        'sys': get_sys(),
    }

    payload = {
        'server': {
            'name': SERVICE_NAME,
            'key': SERVICE_KEY,
        },
        'info': info,
        'errors': {},
    }

    for i in range(3):
        try:
            req = requests.post(API_ENDPOINT, data=json.dumps(payload))
            resp = req.json()
            if resp['success']:
                return
        except Exception as e:
            timestamp = int(time.time())
            payload['errors'][time.time()] = str(e)

    # ME: what should we do?
    # ???: nothing except just eating popcorn


if __name__ == '__main__':
    main()
