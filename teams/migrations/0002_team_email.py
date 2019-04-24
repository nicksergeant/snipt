# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("teams", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name='team',
            name='email',
            field=models.EmailField(default='nick@snipt.net', max_length=255),
            preserve_default=False,
        )
    ]
