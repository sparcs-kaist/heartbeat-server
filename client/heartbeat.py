# Heartbeat Client for SPARCS Services
# Version 0.0.1 - 2016-09-18


import json
import psutil
import pprint
import time
import requests


NETWORK_REPORT = False
SERVICE_NAME = ''
SERVICE_KEY = ''
API_ENDPOINT = 'https://'


# get cpu info
# - user, system, idle (1 sec)
def get_cpu():
    cpu = psutil.cpu_times_percent(interval=1, percpu=False)

    info = {
        'user': cpu.user,
        'system': cpu.system,
        'idle': cpu.idle,
    }

    return info


# get memory info
# - virtual (total, available, used)
# - swap (total, used)
def get_mem():
    virt_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()

    info = {
        'virtual': {
            'total': virt_mem.total,
            'available': virt_mem.available,
            'used': virt_mem.used,
        },
        'swap': {
            'total': swap_mem.total,
            'used': swap_mem.used,
        },
    }

    return info


# get disk info
# - devide (mountpoint, fstype, total, used)
def get_disk():
    info = {}

    disk_list = psutil.disk_partitions()
    for disk in disk_list:
        usage = psutil.disk_usage(disk.mountpoint)
        info[disk.device] = {
            'mountpoint': disk.mountpoint,
            'fstype': disk.fstype,
            'total': usage.total,
            'used': usage.used,
        }

    return info

# get network info
# - bytes (sent, recv) (1 sec)
# - packet (sent, recv) (1 sec)
def get_net():
    info = {
        'bytes_sent': 0,
        'bytes_recv': 0,
        'packets_sent': 0,
        'packets_recv': 0,
    }

    c1 = psutil.net_io_counters()
    time.sleep(1)
    c2 = psutil.net_io_counters()

    info['bytes_sent'] = c2.bytes_sent - c1.bytes_sent
    info['bytes_recv'] = c2.bytes_recv - c1.bytes_recv
    info['packets_sent'] = c2.packets_sent - c1.packets_sent
    info['packets_recv'] = c2.packets_recv - c1.packets_recv

    return info


# get process info
# - name (top 5 cpu usages)
# - name (top 5 mem usages)
def get_proc():
    proc_list = []
    for p in psutil.process_iter():
        try:
            proc_list.append({
                'name': p.name(),
                'cpu': p.cpu_percent(),
                'mem': p.memory_percent(),
            })
        except:
            pass

    def top_n(n, l, key):
        return map(lambda x: x['name'],
                   list(reversed(sorted(l, key=key)))[:n])

    info = {
        'top_cpu': top_n(5, proc_list, lambda x: x['cpu']),
        'top_mem': top_n(5, proc_list, lambda x: x['mem']),
    }

    return info


# get system info
# - boot time
def get_sys():
    info = {
        'boot_time': psutil.boot_time()
    }

    return info


# report info to server
def report(info):
    payload = {
        'server': {
            'name': SERVICE_NAME,
            'key': SERVICE_KEY,
        },
        'info': info,
        'errors': {},
    }

    for i in range(3):
        timestamp = int(time.time())
        try:
            req = requests.post(API_ENDPOINT, data=json.dumps(payload))
            resp = req.json()
            if 'success' in resp:
                return resp['success']
            else:
                error = resp['error'] if 'error' in resp else 'unknown'
                payload['errors'][timestamp] = error

        except Exception as e:
            payload['errors'][timestamp] = str(e)

    return False


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


    if NETWORK_REPORT:
        success = report(info)
        # ME: if fail, what should we do?
        # ???: nothing except just eating popcorn
    else:
        pprint.pprint(info)

if __name__ == '__main__':
    main()
