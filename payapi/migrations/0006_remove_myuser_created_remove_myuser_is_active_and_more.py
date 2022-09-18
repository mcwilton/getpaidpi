# Generated by Django 4.1.1 on 2022-09-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payapi", "0005_remove_myuser_business_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="myuser",
            name="created",
        ),
        migrations.RemoveField(
            model_name="myuser",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="myuser",
            name="is_admin",
        ),
        migrations.RemoveField(
            model_name="myuser",
            name="modified",
        ),
        migrations.AddField(
            model_name="myuser",
            name="merchant_name",
            field=models.CharField(default="", max_length=250),
        ),
        migrations.AddField(
            model_name="myuser",
            name="phone",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AlterField(
            model_name="myuser",
            name="email",
            field=models.EmailField(default="", max_length=254, unique=True),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]
