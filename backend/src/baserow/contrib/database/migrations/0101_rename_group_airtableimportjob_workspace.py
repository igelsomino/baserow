# Generated by Django 3.2.13 on 2023-01-16 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0043_rename_group_workspace"),
        ("database", "0100_airtableimportjob_user_ip_address"),
    ]

    operations = [
        migrations.RenameField(
            model_name="airtableimportjob",
            old_name="group",
            new_name="workspace",
        ),
    ]
