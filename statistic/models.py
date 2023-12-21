from django.db import models


class Platform(models.TextChoices):
    PK = "pk", "pk"
    MOBILE = "mobile", "mobile"
    CONSOLE = "console", "console"


class Game(models.Model):
    logo = models.ImageField(upload_to="logos", blank=True, verbose_name="Логотип")
    title = models.CharField(max_length=256, unique=True, verbose_name="Название")
    platforms = models.CharField(
        max_length=300,
        choices=Platform.choices,
        default=Platform.PK,
        verbose_name="Платформа",
    )

    class Meta:
        verbose_name = "Игры"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Team(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    logo = models.ImageField(upload_to="logo", blank=True, verbose_name="Логотип")
    game = models.ForeignKey(
        Game,
        on_delete=models.DO_NOTHING,
        related_name="teams",
        verbose_name="дисциплина",
    )
    region = models.CharField(max_length=100, blank=True, verbose_name="Регион")
    total_prize = models.PositiveIntegerField(blank=True, verbose_name="Общие призовые")

    class Meta:
        verbose_name = "Команды"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Tournaments(models.Model):
    TYPE_PLATFORM = (("mobile", "mobile"), ("pk", "pk"))
    title = models.CharField(max_length=256, verbose_name="Название")
    image = models.ImageField(upload_to="tournaments", blank=True, verbose_name="Изображение")
    event_date = models.DateTimeField(blank=True, verbose_name="Дата ивента")
    type_platform = models.CharField(
        max_length=100, choices=TYPE_PLATFORM, blank=True, verbose_name="Платформа"
    )
    prize_fond = models.PositiveIntegerField(blank=True, verbose_name="Призовой фонд")
    is_active = models.BooleanField(default=False, verbose_name="Активно")

    class Meta:
        verbose_name = "Турниры"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Player(models.Model):
    username = models.CharField(max_length=256, verbose_name="Имя игрока")
    avatar = models.ImageField(upload_to="avatars", blank=True, verbose_name="Аватар")
    game = models.ForeignKey(
        Game,
        on_delete=models.DO_NOTHING,
        related_name="players",
        verbose_name="Дисциплина",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="players",
        verbose_name="Команда"
    )
    region = models.CharField(max_length=100, blank=True, verbose_name="Регион")
    total_prize = models.PositiveIntegerField(blank=True, verbose_name="Общие призовые")

    class Meta:
        verbose_name = "Игроки"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
