from django.test import TestCase, Client
# from django.test.utils import setup_test_environment
from apps.core.models import Server
import json
# Create your tests here.

class UpdateTestCase(TestCase):
    def setUp(self):
        server = Server.objects.create(name='otlplus', key='abcdefgsecret')
        server.save()
        # setup_test_environment()
        self.c = Client()
        
    def test_valid_reqeust(self):
        r = r'''{ 'server': { 'name': 'otlplus', 'key': 'abcdefgsecret', }, 'info': { {'cpu': {'idle': 99.5, 'system': 0.0, 'user': 0.2}, # cpu percent (all core) 'disk': {'/dev/sda1': {'fstype': 'ext4', # file system type 'mountpoint': '/', # mount point path 'total': 49079525376, # total storage (in byte) 'used': 8587202560}, # used space (in byte) '/dev/sda3': {'fstype': 'vfat', 'mountpoint': '/boot/efi', 'total': 998371328, 'used': 3756032}, '/dev/sda4': {'fstype': 'ext4', 'mountpoint': '/home', 'total': 98294312960, 'used': 7007547392}, '/dev/sda5': {'fstype': 'ext4', 'mountpoint': '/data', 'total': 1181036187648, 'used': 35047948288}, '/dev/sda6': {'fstype': 'ext4', 'mountpoint': '/backup', 'total': 631009894400, 'used': 1335599104}}, 'mem': {'swap': {'total': 8192520192L, 'used': 0L}, # swap memory (in byte) 'virtual': {'available': 7443513344L, # main memory (in byte) 'total': 8313188352L, 'used': 2324901888L}}, 'net': {'bytes_recv': 540, # byte receviced for 1 sec (in byte) 'bytes_sent': 0, 'packets_recv': 9, 'packets_sent': 0}, 'proc': {'top_cpu': # display top 5 process (decreasing order) [{'cpu': 0.0, # cpu usage (in percentage) 'mem': 0.10031597561474329, # memory usage (in percentage) 'name': 'zsh'}, # process name {'cpu': 0.0, 'mem': 0.05257227209279524, 'name': 'sshd'}, {'cpu': 0.0, 'mem': 0.08188858127293878, 'name': 'sshd'}, {'cpu': 0.0, 'mem': 0.0, 'name': 'kworker/1:0'}, {'cpu': 0.0, 'mem': 0.0, 'name': 'kworker/1:2'}], 'top_mem': # display top 5 process (decreasing order) [{'cpu': 0.0, 'mem': 1.6681226279041006, 'name': 'mysqld'}, {'cpu': 0.0, 'mem': 0.7871059481559549, 'name': 'unity-greeter'}, {'cpu': 0.0, 'mem': 0.5006437270242665, 'name': 'Xorg'}, {'cpu': 0.0, 'mem': 0.44816999714720285, 'name': 'apache2'}, {'cpu': 0.0, 'mem': 0.4470367616662897, 'name': 'apache2'}]}, 'sys': {'boot_time': 1475482648.0} # boot time (in unix timestamp) }, 'errors': { # errors 'key is unix timestamp': 'value is obtained by str(e)', '1475855554': 'Invalid URL u\'https://\': No host supplied', '1475855549': 'Invalid URL u\'https://\': No host supplied', '1475855559': 'Invalid URL u\'https://\': No host supplied', } } '''


        res = self.c.post('/api/update/', r, content_type='application/json')

        self.assertEqual(res.json(), {'success': True})
