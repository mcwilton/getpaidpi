# Generated by Django 4.1.1 on 2022-09-19 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_remove_customuser_username_alter_profile_merchant_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="profile",
            name="merchant_id",
            field=models.DecimalField(
                decimal_places=0, default="45637291", max_digits=10
            ),
        ),
    ]
