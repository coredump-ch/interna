# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('phone', models.CharField(max_length=16, blank=True)),
                ('city', models.CharField(help_text='Wohnort', max_length=100, blank=True)),
                ('twitter', models.CharField(help_text='Twitter Benutzername', max_length=32, blank=True)),
                ('github', models.CharField(help_text='Github Benutzername', max_length=32, blank=True)),
            ],
            options={
                'ordering': ('name', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateField()),
                ('end', models.DateField(null=True, blank=True)),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'Verdiener'), (2, 'Nichtverdiener')])),
                ('paid_until', models.CharField(max_length=4, blank=True)),
                ('ccc', models.BooleanField(default=False, help_text='CCC Mitglied?')),
                ('Member', models.ForeignKey(related_name='Membership', to='memberdb.Member', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('-start', '-Member__pk'),
                'get_latest_by': ('end', 'start'),
            },
        ),
    ]
