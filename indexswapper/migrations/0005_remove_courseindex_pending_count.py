# Generated by Django 4.2.1 on 2023-07-02 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("indexswapper", "0004_swaprequest_index_gained"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="courseindex",
            name="pending_count",
        ),
    ]
