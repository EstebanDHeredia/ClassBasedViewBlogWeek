# Generated by Django 4.2.11 on 2024-05-24 22:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0003_alter_post_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Me gusta",
            ),
        ),
    ]
