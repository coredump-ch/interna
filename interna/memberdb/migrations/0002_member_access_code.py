# -*- coding: utf-8 -*-


from django.db import migrations, models
try:
    import memberdb.access_codes
    generate = memberdb.access_codes.generate_access_code
except ImportError:
    def generate(*args, **kwargs):
        return 'gone'


class Migration(migrations.Migration):

    dependencies = [
        ('memberdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='access_code',
            field=models.CharField(default=generate, help_text='Passphrase to open the hackerspace door', max_length=100, blank=True),
        ),
    ]
