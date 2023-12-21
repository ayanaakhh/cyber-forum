# Generated by Django 4.2.8 on 2023-12-20 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("statistic", "0004_remove_game_genre_alter_game_platforms"),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=256, verbose_name="Имя игрока"),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, upload_to="avatars", verbose_name="Аватар"
                    ),
                ),
                (
                    "region",
                    models.CharField(blank=True, max_length=100, verbose_name="Регион"),
                ),
                (
                    "total_prize",
                    models.PositiveIntegerField(
                        blank=True, verbose_name="Общие призовые"
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="players",
                        to="statistic.game",
                        verbose_name="Дисциплина",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="players",
                        to="statistic.team",
                        verbose_name="Команда",
                    ),
                ),
            ],
            options={
                "verbose_name": "Игроки",
                "verbose_name_plural": "Игроки",
            },
        ),
    ]