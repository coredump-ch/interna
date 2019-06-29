# Generated by Django 2.2.2 on 2019-06-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('identifier', models.CharField(help_text='A short lowercase identifier, e.g. "um2"', max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='A short name, e.g. "Ultimaker 2+"', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Describe this item')),
                ('owner', models.CharField(help_text='Who owns this item? If it belongs to the hackerspace, set this value to "Coredump".', max_length=255)),
                ('category', models.CharField(blank=True, choices=[('manufacturing', '3D Printing, Scanning, Cutting, Plotting'), ('computers_network', 'Computers & Networking'), ('electronics_lab', 'Electronics Lab'), ('home_appliances', 'Home Appliances'), ('vintage', 'Vintage Computers')], help_text='In what category does this device belong?', max_length=255, null=True)),
                ('since', models.DateField(blank=True, help_text='When was this item brought to the hackerspace?', null=True)),
                ('cost', models.IntegerField(blank=True, help_text='How much did this cost us?', null=True)),
                ('howto_url', models.URLField(blank=True, help_text='An URL to a page that explains how to use this item', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
