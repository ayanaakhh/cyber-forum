from django.contrib import admin

from .models import Game, Team, Tournaments, Player


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "platforms",
    )
    search_fields = ["title", ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "game",
        "region",
        "total_prize",
    )
    search_fields = ["title", "region"]


@admin.register(Tournaments)
class TournamentsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "event_date",
        "type_platform",
        "prize_fond",
        "is_active",
    )
    search_fields = ["title", "type_platform"]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "game",
        "region",
        "total_prize",
    ]
    search_fields = ["username", "region"]
