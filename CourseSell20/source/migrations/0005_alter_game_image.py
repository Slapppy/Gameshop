# Generated by Django 4.2.1 on 2023-05-21 00:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("source", "0004_alter_game_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="image",
            field=models.ImageField(upload_to="static/images"),
        ),
    ]
