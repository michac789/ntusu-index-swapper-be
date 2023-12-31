# Generated by Django 4.2.1 on 2023-07-03 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("indexswapper", "0006_courseindex_pending_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="swaprequest",
            name="contact_type",
            field=models.CharField(
                choices=[("E", "Email"), ("T", "Telegram"), ("P", "Phone")],
                default="E",
                max_length=1,
            ),
            preserve_default=False,
        ),
    ]
