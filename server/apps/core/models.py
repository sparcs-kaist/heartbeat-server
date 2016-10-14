from django.db import models

# Create your models here.

ProcessUsage_Type = (
        ('C','CPU'),
        ('M','Memory'),
)

# To-do 
# Server class should have the attribute about backup status
class Server(models.Model):
    name = models.CharField(unique=True, max_length=30)
    alias = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    key = models.CharField(max_length=255)

class UsageLog(models.Model):
    server = models.ForeignKey('Server', db_index=True)
    datetime = models.DateTimeField() # 서버에서 저장시간 or client들이 정보 얻을때의 시간?
    
class CpuUsage(models.Model):
    usagelog = models.ForeignKey('UsageLog', db_index=True)
    user = models.DecimalField(max_digits=20, decimal_places=3) # 100%는 어떻게함
    system = models.DecimalField(max_digits=20, decimal_places=3)
    idle = models.DecimalField(max_digits=20, decimal_places=3)

class MemoryUsage(models.Model):
    usagelog = models.ForeignKey('UsageLog', db_index=True)
    swap_total = models.BigIntegerField() # byte
    swap_used = models.BigIntegerField() # byte
    virt_avail = models.BigIntegerField() # byte
    virt_used = models.BigIntegerField() # byte
    virt_total = models.BigIntegerField()
    
class DiskUsage(models.Model):
    usagelog = models.ForeignKey('UsageLog', db_index=True)
    device_name = models.CharField(max_length=30) # ex) dev/sda ...
    fs_type = models.CharField(max_length=10) # Filesystem type
    mount_point = models.CharField(max_length=30) # Disk mount path
    used = models.IntegerField() # byte
    total = models.IntegerField() # byte

class ProcessUsage(models.Model): 
    ProcessUsage_Type = (
        ('C','CPU'),
        ('M','Memory'),
    )

    usagelog = models.ForeignKey('UsageLog', db_index=True)
    name = models.CharField(max_length=127)
    order = models.IntegerField() #top 10 order
    cpu = models.DecimalField(max_digits=20, decimal_places=3)
    memory = models.DecimalField(max_digits=20, decimal_places=3)
    type = models.CharField(max_length=1, choices=ProcessUsage_Type)

class ErrorLog(models.Model):
    usagelog = models.ForeignKey('UsageLog', db_index=True)
    datetime = models.DateTimeField() # 서버저장시간 or client 정보 획슫 시간?
    log = models.TextField()
