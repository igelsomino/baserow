# Generated by Django 2.2.11 on 2020-05-22 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0005_auto_20200505_1242"),
    ]

    operations = [
        migrations.CreateModel(
            name="LongTextField",
            fields=[
                (
                    "field_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="database.Field",
                    ),
                ),
            ],
            bases=("database.field",),
        ),
        migrations.AlterModelOptions(
            name="gridviewfieldoptions",
            options={"ordering": ("field_id",)},
        ),
    ]
