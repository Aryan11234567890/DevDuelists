# Generated by Django 5.0.6 on 2024-07-23 04:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MyApp", "0007_alter_code_result"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="problem",
            name="hidden_tc",
        ),
        migrations.AddField(
            model_name="problem",
            name="expected_output",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="problem",
            name="hidden_input",
            field=models.TextField(default="xD"),
        ),
    ]
