# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snipts', '0003_snipt_last_user_saved'),
    ]

    operations = [
        migrations.AddField(
            model_name='snipt',
            name='secure',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='snipt',
            name='title',
            field=models.CharField(max_length=255, blank=True, null=True, default='Untitled'),
        ),
    ]
