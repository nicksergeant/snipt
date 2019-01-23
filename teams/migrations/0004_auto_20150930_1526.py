# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [("teams", "0003_auto_20150818_0057")]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(
                related_name="member", to=settings.AUTH_USER_MODEL, blank=True
            ),
        )
    ]
