# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-15 13:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0007_auto_20160715_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='shapefile',
            name='layerName2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='maps.Layers'),
            preserve_default=False,
        ),
    ]
