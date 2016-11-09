# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-08 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackupLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('success', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='BackupTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('period', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CpuUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.DecimalField(decimal_places=3, max_digits=20)),
                ('system', models.DecimalField(decimal_places=3, max_digits=20)),
                ('idle', models.DecimalField(decimal_places=3, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='DiskUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=30)),
                ('fs_type', models.CharField(max_length=10)),
                ('mount_point', models.CharField(max_length=30)),
                ('used', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('log', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MemoryUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('swap_total', models.BigIntegerField()),
                ('swap_used', models.BigIntegerField()),
                ('virt_avail', models.BigIntegerField()),
                ('virt_used', models.BigIntegerField()),
                ('virt_total', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProcessUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('order', models.IntegerField()),
                ('cpu', models.DecimalField(decimal_places=3, max_digits=20)),
                ('memory', models.DecimalField(decimal_places=3, max_digits=20)),
                ('type', models.CharField(choices=[('C', 'CPU'), ('M', 'Memory')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('alias', models.CharField(max_length=255)),
                ('ip', models.GenericIPAddressField()),
                ('key', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UsageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Server')),
            ],
        ),
        migrations.AddField(
            model_name='processusage',
            name='usagelog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UsageLog'),
        ),
        migrations.AddField(
            model_name='memoryusage',
            name='usagelog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UsageLog'),
        ),
        migrations.AddField(
            model_name='errorlog',
            name='usagelog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UsageLog'),
        ),
        migrations.AddField(
            model_name='diskusage',
            name='usagelog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UsageLog'),
        ),
        migrations.AddField(
            model_name='cpuusage',
            name='usagelog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UsageLog'),
        ),
        migrations.AddField(
            model_name='backuptarget',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Server'),
        ),
        migrations.AddField(
            model_name='backuplog',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Server'),
        ),
        migrations.AddField(
            model_name='backuplog',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.BackupTarget'),
        ),
    ]