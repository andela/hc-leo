# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-11 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20180611_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='status',
            field=models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('new', 'New'), ('paused', 'Paused'), ('often', 'Often')], default='new', max_length=6),
        ),
    ]
