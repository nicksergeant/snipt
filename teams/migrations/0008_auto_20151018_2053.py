# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_team_disabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='plan',
            field=models.CharField(default=b'snipt-teams-25-monthly', max_length=100, null=True, blank=True, choices=[(b'snipt-teams-25-monthly', b'25 users, monthly'), (b'snipt-teams-100-monthly', b'100 users, monthly'), (b'snipt-teams-250-monthly', b'250 users, monthly'), (b'snipt-teams-unlimited-monthly', b'Unlimited users, monthly'), (b'snipt-teams-25-yearly', b'25 users, yearly'), (b'snipt-teams-100-yearly', b'100 users, yearly'), (b'snipt-teams-250-yearly', b'250 users, yearly'), (b'snipt-teams-unlimited-yearly', b'Unlimited users, yearly')]),
        ),
    ]
