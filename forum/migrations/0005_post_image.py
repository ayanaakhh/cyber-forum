# Generated by Django 5.0 on 2023-12-09 07:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0004_alter_comment_options_alter_post_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="previews/", verbose_name="изображение"
            ),
        ),
    ]
