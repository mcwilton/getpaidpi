# Generated by Django 4.1.1 on 2022-09-16 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payapi", "0002_remove_myuser_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
