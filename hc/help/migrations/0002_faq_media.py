# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-19 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='media',
            field=models.CharField(max_length=500, null=True),
        ),
    ]