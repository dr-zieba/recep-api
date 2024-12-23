# Generated by Django 4.2.7 on 2024-10-22 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                error_messages={"Invalid Value": "Email already exists"},
                max_length=255,
                unique=True,
            ),
        ),
    ]
