# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-15 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_auto_20160701_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idLayer', models.CharField(max_length=120)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.AlterField(
            model_name='shapefile',
            name='layerName',
            field=models.CharField(choices=[(b'border', b'hranice'), (b'state', b'Staty'), (b'state-by-city', b'Staty skrze hlavni mesta'), (b'region', b'Regiony'), (b'province', b'Provincie'), (b'region_cz', b'Kraje'), (b'region_it', b'Oblasti'), (b'autonomous_Comunity', b'Autonomni spolecenstvi'), (b'bundesland', b'Spolkove zeme'), (b'city', b'Mesta'), (b'city-by-state', b'Hlavni mesta skrze staty'), (b'river', b'Reky'), (b'reservoir', b'Vodni nadrze'), (b'lake', b'Jezera'), (b'sea', b'More'), (b'mountains', b'Pohori'), (b'surface', b'Povrch'), (b'island', b'Ostrovy')], max_length=120, null=True),
        ),
    ]
