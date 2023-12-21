import os

import django
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from forum.models import Post

User = get_user_model()


def get_soup(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None


def extract_links(soup):
    links = []
    all_news = soup.find("div", class_="list_t3W3E").find_all(
        "article", class_="article_TR7k-"
    )

    for elem in all_news:
        link = elem.find("a")
        href = link.get("href") if link else None
        preview = link.find("img").get("src") if link else None
        if href:
            links.append(
                {"link": "https://www.cybersport.ru" + href, "preview": preview}
            )

    return links


def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error during image download: {e}")
        return None


def get_post_data(post: dict) -> dict:
    soup = get_soup(post["link"])
    if soup:
        title_tag = soup.find("h1")
        text_tag = soup.find(
            "div",
            class_="text-content js-mediator-article js-mediator-article root_sK2zH content_5HuK5",
        )

        post["title"] = title_tag.text.strip() if title_tag else None
        post["text"] = text_tag.text.strip() if text_tag else None

    return post


def fill_data_model(posts):
    for post in posts:
        title = post["title"]
        if title:
            image_content = download_image(post["preview"])
            if image_content:
                obj, created = Post.objects.get_or_create(
                    title=title,
                    defaults={
                        "image": ContentFile(image_content, name=f"{title}_image.jpg"),
                        "text": post["text"],
                        "author": User.objects.all().first() or None,
                    },
                )
                if not created:
                    obj.title = title
                    obj.image.save(
                        f"{title}_image.jpg",
                        ContentFile(image_content, name=f"{title}_image.jpg"),
                        save=True,
                    )
                    obj.text = post["text"]
                    obj.author = User.objects.all().first() or None
                    obj.save()


url = "https://www.cybersport.ru/blog"
soup = get_soup(url)

if soup:
    links = extract_links(soup)
    new_posts = [get_post_data(link) for link in links]
    fill_data_model(new_posts)
