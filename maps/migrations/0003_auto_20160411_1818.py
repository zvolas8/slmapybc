# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import maps.models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_auto_20160410_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='SvgFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('config', models.TextField()),
                ('filesvg', models.FileField(blank=True, null=True, upload_to=maps.models.uploadLocation)),
            ],
        ),
        migrations.AlterField(
            model_name='shapefile',
            name='fileshp',
            field=models.FileField(blank=True, null=True, upload_to=maps.models.uploadLocation),
        ),
    ]
