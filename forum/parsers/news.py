import os

import django
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from forum.models import News


def fill_data_model(news_posts):
    for news in news_posts:
        title = news.get("title")
        if title:
            image_content = download_image(news.get("image"))
            if image_content:
                obj, created = News.objects.get_or_create(
                    title=title,
                    defaults={
                        "image": ContentFile(image_content, name=f"{title}_image.jpg"),
                        "text": news.get("text"),
                    },
                )
                if not created:
                    obj.image.save(
                        f"{title}_image.jpg",
                        ContentFile(image_content, name=f"{title}_image.jpg"),
                        save=True,
                    )
                    obj.text = news.get("text")
                    obj.save()


def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error during image download: {e}")
        return None


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
    all_news = soup.find_all("div", class_="post-list-styles post-list-style-1")

    for elem in all_news:
        link = elem.find("div", class_="title").find("a")
        href = link.get("href") if link else None
        if href:
            links.append(href)

    return links


def get_news_data(link: str) -> dict:
    news = {}
    soup = get_soup(link)

    if soup:
        title_tag = soup.find("h1")
        image_tag = soup.find("div", class_="post-featured-header").find("img")
        text_tags = soup.find("div", class_="post-wrapper").findAll("p")

        news["title"] = title_tag.text.strip() if title_tag else None
        image_url = image_tag.get("src") if image_tag else None
        news["image"] = image_url if image_url else None
        news["text"] = [paragraph for paragraph in text_tags] if text_tags else None

    return news


url = "https://dota2.kg/news/esportskg/"
soup = get_soup(url)

if soup:
    links = extract_links(soup)
    news_posts = [get_news_data(link) for link in links]
    fill_data_model(news_posts)
    print("parsing done!")
