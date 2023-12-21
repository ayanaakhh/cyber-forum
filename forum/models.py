import os
import urllib

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models

User = get_user_model()


class Post(models.Model):
    """модель поста"""

    title = models.CharField(max_length=256, verbose_name="название")
    image = models.ImageField(
        upload_to="previews/", blank=True, verbose_name="изображение"
    )
    text = RichTextField(max_length=10000, verbose_name="текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата публикации")
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="posts",
        verbose_name="автор",
        blank=True,
    )

    class Meta:
        verbose_name = "Посты"
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def get_remote_image(self, image_url):
        result = urllib.urlretrieve(image_url)
        self.image.save(os.path.basename(image_url), File(open(result[0])))
        self.save()


class Comment(models.Model):
    """модель коммента"""

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="пост"
    )
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="comments", verbose_name="автор"
    )
    text = models.TextField(max_length=1000, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    def __str__(self):
        return f"comment id: {self.pk}, author: {self.author}"


class AboutUs(models.Model):
    """О нас"""

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = RichTextField(max_length=100000, verbose_name="Текст")

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "Текстовое наполнение страницы - О нас"


class News(models.Model):
    """Нововсти"""

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    image = models.ImageField(upload_to="news", blank=True, verbose_name="Изображение")
    text = RichTextField(max_length=100000, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    def __str__(self):
        return self.title
