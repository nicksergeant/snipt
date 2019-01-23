# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Snipt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default=b"Untitled", max_length=255, null=True, blank=True
                    ),
                ),
                ("slug", models.SlugField(max_length=255, blank=True)),
                ("custom_slug", models.SlugField(max_length=255, blank=True)),
                ("lexer", models.CharField(max_length=50)),
                ("code", models.TextField()),
                ("meta", models.TextField(null=True, blank=True)),
                ("description", models.TextField(null=True, blank=True)),
                ("stylized", models.TextField(null=True, blank=True)),
                ("stylized_min", models.TextField(null=True, blank=True)),
                ("embedded", models.TextField(null=True, blank=True)),
                (
                    "line_count",
                    models.IntegerField(default=None, null=True, blank=True),
                ),
                ("key", models.CharField(max_length=100, null=True, blank=True)),
                ("public", models.BooleanField(default=False)),
                ("blog_post", models.BooleanField(default=False)),
                ("views", models.IntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("publish_date", models.DateTimeField(null=True, blank=True)),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        to="taggit.Tag",
                        through="taggit.TaggedItem",
                        help_text="A comma-separated list of tags.",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True, to=settings.AUTH_USER_MODEL, null=True
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="favorite",
            name="snipt",
            field=models.ForeignKey(to="snipts.Snipt"),
        ),
        migrations.AddField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
