# Generated by Django 3.2.13 on 2023-02-21 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0103_remove_timezone_form_created_last_modified_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="airtableimportjob",
            name="timezone",
        ),
    ]