from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import localtime
from apps.core.models import Server, BackupTarget, BackupLog
from croniter import croniter
from datetime import datetime, timedelta
import pytz
import os


class Command(BaseCommand):
    help = 'Update a backup status'

    def handle(self, *args, **options):
        now = localtime(timezone.now() - timedelta(minutes=10))
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

            logs = BackupLog.objects.filter(target=target, path=path)
            logs_count = logs.count()
            if path == path_template:
                if logs_count > 0:
                    first_log = logs.first()
                    first_log.datetime = backup_time
                    first_log.size = backup_size
                    first_log.save()
                    continue

            if logs_count == 0:
                BackupLog(server=server, target=target, datetime=backup_time,
                          path=path, size=backup_size).save()
