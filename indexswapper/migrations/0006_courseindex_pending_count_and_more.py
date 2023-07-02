# Generated by Django 4.2.1 on 2023-07-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("indexswapper", "0005_remove_courseindex_pending_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="courseindex",
            name="pending_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="swaprequest",
            name="index_gained",
            field=models.CharField(blank=True, default="", max_length=6),
        ),
    ]
