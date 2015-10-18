# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snipts', '0002_sniptlogentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='snipt',
            name='last_user_saved',
            field=models.ForeignKey(related_name='last_user_saved', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
