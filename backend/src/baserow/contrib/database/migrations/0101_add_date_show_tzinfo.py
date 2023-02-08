# Generated by Django 3.2.13 on 2023-02-08 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0100_airtableimportjob_user_ip_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="createdonfield",
            name="date_show_tzinfo",
            field=models.BooleanField(
                default=False, help_text="Indicates if the timezone should be shown."
            ),
        ),
        migrations.AddField(
            model_name="datefield",
            name="date_show_tzinfo",
            field=models.BooleanField(
                default=False, help_text="Indicates if the timezone should be shown."
            ),
        ),
        migrations.AddField(
            model_name="formulafield",
            name="date_show_tzinfo",
            field=models.BooleanField(
                default=False, help_text="Indicates if the time zone should be shown."
            ),
        ),
        migrations.AddField(
            model_name="lastmodifiedfield",
            name="date_show_tzinfo",
            field=models.BooleanField(
                default=False, help_text="Indicates if the timezone should be shown."
            ),
        ),
    ]