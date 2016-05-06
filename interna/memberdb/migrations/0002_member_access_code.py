# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import memberdb.access_codes


class Migration(migrations.Migration):

    dependencies = [
        ('memberdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='access_code',
            field=models.CharField(default=memberdb.access_codes.generate_access_code, help_text='Passphrase to open the hackerspace door', max_length=100, blank=True),
        ),
    ]
