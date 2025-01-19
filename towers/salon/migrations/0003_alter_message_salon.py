# Generated by Django 5.0.4 on 2025-01-13 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("salon", "0002_remove_salon_description_alter_message_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="salon",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="salon.salon",
            ),
        ),
    ]
