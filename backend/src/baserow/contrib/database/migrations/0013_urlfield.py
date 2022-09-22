# Generated by Django 2.2.11 on 2020-09-27 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0012_auto_20200904_1410"),
    ]

    operations = [
        migrations.CreateModel(
            name="URLField",
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
    ]
