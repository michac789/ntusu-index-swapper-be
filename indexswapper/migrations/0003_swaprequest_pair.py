# Generated by Django 4.2.1 on 2023-07-01 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("indexswapper", "0002_alter_swaprequest_contact_info"),
    ]

    operations = [
        migrations.AddField(
            model_name="swaprequest",
            name="pair",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="indexswapper.swaprequest",
            ),
        ),
    ]
