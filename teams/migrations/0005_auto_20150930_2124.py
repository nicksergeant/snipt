# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("teams", "0004_auto_20150930_1526")]

    operations = [
        migrations.AddField(
            model_name="team",
            name="stripe_id",
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="team", name="name", field=models.CharField(max_length=30)
        ),
    ]
