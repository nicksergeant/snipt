# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("snipts", "0004_auto_20160512_1058"),
    ]

    operations = [
        migrations.CreateModel(
            name="SniptSecureView",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        primary_key=True,
                        auto_created=True,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("snipt", models.ForeignKey(to="snipts.Snipt")),
                ("user", models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        )
    ]
