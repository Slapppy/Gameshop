# Generated by Django 4.1.4 on 2023-07-29 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("source", "0011_alter_game_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="image",
            field=models.ImageField(upload_to="source/static/source/images"),
        ),
    ]
