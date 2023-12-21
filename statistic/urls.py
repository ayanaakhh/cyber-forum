from django.urls import path

from .views import TeamsStatisticView, GamesListView, PlayerStatisticView, TournamentsListView, TournamentDetailView

urlpatterns = [
    path("games", GamesListView.as_view(), name="games"),
    path("game/<int:pk>/teams", TeamsStatisticView.as_view(), name="teams-statistics"),
    path("game/<int:pk>/players", PlayerStatisticView.as_view(), name="players-statistics"),
    path("tournaments", TournamentsListView.as_view(), name="tournaments-list"),
    path("tournament/<int:pk>", TournamentDetailView.as_view(), name="tournament-detail"),
]
