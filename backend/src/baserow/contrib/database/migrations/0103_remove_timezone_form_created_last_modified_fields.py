# Generated by Django 3.2.13 on 2023-02-10 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0102_fix_datetimes_timezones"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="createdonfield",
            name="timezone",
        ),
        migrations.RemoveField(
            model_name="lastmodifiedfield",
            name="timezone",
        ),
    ]
