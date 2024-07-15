# Generated by Django 5.0.6 on 2024-07-14 17:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MyApp", "0002_delete_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="difficulty",
            field=models.CharField(default="Medium", max_length=50),
        ),
        migrations.AddField(
            model_name="problem",
            name="frequency",
            field=models.IntegerField(default=0),
        ),
    ]
