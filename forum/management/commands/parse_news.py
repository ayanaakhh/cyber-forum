from django.core.management.base import BaseCommand

from forum.parsers.news import (extract_links, fill_data_model, get_news_data,
                                get_soup)


class Command(BaseCommand):
    help = "Парсинг новостей"

    def handle(self, *args, **options):
        url = "https://dota2.kg/news/esportskg/"
        soup = get_soup(url)

        if soup:
            links = extract_links(soup)
            news_posts = [get_news_data(link) for link in links]
            fill_data_model(news_posts)
            self.stdout.write(self.style.SUCCESS("Парсинг новостей завершен!"))
