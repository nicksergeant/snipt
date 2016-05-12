# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150724_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='blog_theme',
            field=models.CharField(max_length=1, choices=[('D', 'Default'), ('A', 'Pro Adams')], default='A'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='default_editor',
            field=models.CharField(max_length=250, choices=[('C', 'CodeMirror'), ('T', 'Textarea')], default='C'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='editor_theme',
            field=models.CharField(max_length=250, choices=[('default', 'Default'), ('ambiance', 'Ambiance'), ('blackboard', 'Blackboard'), ('cobalt', 'Cobalt'), ('eclipse', 'Eclipse'), ('elegant', 'Elegant'), ('erlang-dark', 'Erlang Dark'), ('lesser-dark', 'Lesser Dark'), ('monokai', 'Monokai'), ('neat', 'Neat'), ('night', 'Night'), ('rubyblue', 'Ruby Blue'), ('solarized dark', 'Solarized Dark'), ('solarized light', 'Solarized Light'), ('twilight', 'Twilight'), ('vibrant-ink', 'Vibrant Ink'), ('xq-dark', 'XQ Dark')], default='default'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='list_view',
            field=models.CharField(max_length=1, choices=[('N', 'Normal'), ('C', 'Compact')], default='N'),
        ),
    ]
