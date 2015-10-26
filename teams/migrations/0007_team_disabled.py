# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_team_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
