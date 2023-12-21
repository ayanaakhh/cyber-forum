from django.utils import timezone
from django.views import generic

from .models import Game, Team, Player, Tournaments


class GamesListView(generic.ListView):
    model = Game
    template_name = "games_list.html"
    context_object_name = "games"


class TeamsStatisticView(generic.DetailView):
    model = Game
    template_name = "top_commands.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        teams = Team.objects.filter(game=game).order_by("-total_prize")
        players = Player.objects.filter(game=game).order_by("-total_prize")
        context["teams"] = teams
        context["players"] = players
        return context


class PlayerStatisticView(generic.DetailView):
    model = Game
    template_name = "top_players.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        players = Player.objects.filter(game=game).order_by("-total_prize")
        context["players"] = players
        return context


class TournamentsListView(generic.ListView):
    model = Tournaments
    template_name = "tournaments.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        Tournaments.objects.filter(event_date__lt=timezone.now()).update(is_active=False)
        return Tournaments.objects.all()


class TournamentDetailView(generic.DetailView):
    model = Tournaments
    template_name = "tournament_detail.html"
    context_object_name = "tournament"
