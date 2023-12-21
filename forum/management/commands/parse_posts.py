from django.core.management.base import BaseCommand

from forum.parsers.posts import (extract_links, fill_data_model, get_post_data,
                                 get_soup)


class Command(BaseCommand):
    help = "Парсинг постов"

    def handle(self, *args, **options):
        url = "https://www.cybersport.ru/blog"
        soup = get_soup(url)

        if soup:
            links = extract_links(soup)
            new_posts = [get_post_data(link) for link in links]
            fill_data_model(new_posts)
            self.stdout.write(self.style.SUCCESS("Парсинг постов завершен!"))
