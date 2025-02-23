# Generated by Django 4.2.18 on 2025-01-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("memberdb", "0005_member_key_number_member_key_safe"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="key_safe",
            field=models.CharField(
                blank=True,
                choices=[("app", "App"), ("code", "Code"), ("none", "Nein")],
                help_text="Art des Schlüsselsafe-Zugriffs",
                max_length=100,
            ),
        ),
    ]
