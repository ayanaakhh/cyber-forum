import os
from pprint import pprint

import django
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from statistic.models import Team, Game

User = get_user_model()


dota = Game.objects.get_or_create(title="Dota 2",)


def get_soup(link):
    try:
        page = requests.get(link)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None


def get_teams_data(link) -> dict:
    soup = get_soup(link)
    team = dict()

    if soup:
        teams = soup.find("tbody", class_='tbody_p42Mg').findAll("tr")
        for tag in teams:
            title_tag = tag.find("a").find("div", _class="")
            tp_tag = soup.find(
                "td",
                class_="cellTotal_1yo3T cellTotalText_yck9n",
            )
            team["title"] = title_tag.text.strip() if title_tag else None
            team["total_prize"] = tp_tag.text.strip() if tp_tag else None

    return team


url = 'https://www.cybersport.ru/teams/dota-2'

soup = get_soup(url)

if soup:
    teams = get_teams_data(url)
    pprint(teams)
    # links = extract_links(soup)
    # new_posts = [get_post_data(link) for link in links]
    # fill_data_model(new_posts)
