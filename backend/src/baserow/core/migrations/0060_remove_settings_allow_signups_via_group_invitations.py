# Generated by Django 3.2.13 on 2023-02-13 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0059_migrate_allow_signups_via_workspace_invitations"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="settings",
            name="allow_signups_via_group_invitations",
        ),
    ]
