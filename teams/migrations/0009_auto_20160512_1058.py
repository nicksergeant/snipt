# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_auto_20151018_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='plan',
            field=models.CharField(max_length=100, choices=[('snipt-teams-25-monthly', '25 users, monthly'), ('snipt-teams-100-monthly', '100 users, monthly'), ('snipt-teams-250-monthly', '250 users, monthly'), ('snipt-teams-unlimited-monthly', 'Unlimited users, monthly'), ('snipt-teams-25-yearly', '25 users, yearly'), ('snipt-teams-100-yearly', '100 users, yearly'), ('snipt-teams-250-yearly', '250 users, yearly'), ('snipt-teams-unlimited-yearly', 'Unlimited users, yearly')], blank=True, null=True, default='snipt-teams-25-monthly'),
        ),
    ]
