from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import localtime
from apps.core.models import Server, BackupTarget, BackupLog
from croniter import croniter
from datetime import datetime
import pytz
import os


class Command(BaseCommand):
    help = 'Update a backup status'

    def handle(self, *args, **options):
        now = localtime(timezone.now())
        targets = BackupTarget.objects.all()
        for target in targets:
            server, path_template, period = \
                target.server, target.path_template, target.period

            should_last_time = croniter(period, now).get_prev(datetime)
            path = path_template.format(time=should_last_time)

            if not os.path.exists(path):
                continue

            local_tz = pytz.timezone('Asia/Seoul')
            backup_time = datetime.fromtimestamp(os.path.getmtime(path)).replace(tzinfo=local_tz)
            backup_size = os.path.getsize(path)

            logs_count = BackupLog.objects.filter(target=target, path=path).count()
            if logs_count > 0 and path != path_template:
                continue

            BackupLog(server=server, target=target, datetime=backup_time,
                      path=path, size=backup_size).save()
