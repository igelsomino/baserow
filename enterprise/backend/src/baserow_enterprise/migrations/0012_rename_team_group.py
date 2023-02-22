# Generated by Django 3.2.13 on 2023-01-17 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0051_rename_group_installtemplatejob_workspace"),
        ("baserow_enterprise", "0011_audit_log"),
    ]

    operations = [
        migrations.RenameField(
            model_name="team",
            old_name="group",
            new_name="workspace",
        ),
        migrations.AlterUniqueTogether(
            name="team",
            unique_together={("name", "workspace")},
        ),
    ]
