# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-06-24 21:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberdb', '0002_member_access_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='access_code',
        ),
    ]
