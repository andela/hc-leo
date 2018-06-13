# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-11 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_check_nagging_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='allowed_nagging',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='check',
            name='next_nagging',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]