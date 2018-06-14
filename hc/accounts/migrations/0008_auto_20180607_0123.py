# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-07 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180606_0206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='reports_allowed_period',
            new_name='reports_period',
        ),
        migrations.AddField(
            model_name='profile',
            name='reports_allowed',
            field=models.BooleanField(default=True),
        ),
    ]