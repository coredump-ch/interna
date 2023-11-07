# Generated by Django 1.11.4 on 2017-08-20 22:36
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crowdfund', '0003_auto_20170821_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='initiator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
