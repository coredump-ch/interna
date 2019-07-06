# Generated by Django 2.2.2 on 2019-06-29 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20190629_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='manager',
            field=models.CharField(blank=True, help_text='Who should you ask if you have questions about this item?', max_length=255, null=True),
        ),
    ]