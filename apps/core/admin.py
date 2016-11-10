from django.contrib import admin
from apps.core.models import Server, UsageLog, BackupTarget


class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'ip', )


class BackupTargetAdmin(admin.ModelAdmin):
    list_display = ('server', 'path', 'period', )


admin.site.register(UsageLog)
admin.site.register(Server, ServerAdmin)
admin.site.register(BackupTarget, BackupTargetAdmin)
