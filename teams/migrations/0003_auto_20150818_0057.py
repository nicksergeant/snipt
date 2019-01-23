# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [("teams", "0002_team_email")]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="user",
            field=models.OneToOneField(
                null=True, blank=True, to=settings.AUTH_USER_MODEL
            ),
        )
    ]
