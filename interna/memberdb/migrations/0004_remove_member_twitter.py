# Generated by Django 4.2.18 on 2025-01-22 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("memberdb", "0003_remove_member_access_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="twitter",
        ),
    ]
