# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_pro', models.BooleanField(default=False)),
                ('teams_beta_seen', models.BooleanField(default=False)),
                ('teams_beta_applied', models.BooleanField(default=False)),
                ('pro_date', models.DateTimeField(null=True, blank=True)),
                ('stripe_id', models.CharField(max_length=100, null=True, blank=True)),
                ('has_gravatar', models.BooleanField(default=False)),
                ('list_view', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'Normal'), (b'C', b'Compact')])),
                ('blog_title', models.CharField(max_length=250, null=True, blank=True)),
                ('blog_theme', models.CharField(default=b'A', max_length=1, choices=[(b'D', b'Default'), (b'A', b'Pro Adams')])),
                ('blog_domain', models.CharField(max_length=250, null=True, blank=True)),
                ('default_editor', models.CharField(default=b'C', max_length=250, choices=[(b'C', b'CodeMirror'), (b'T', b'Textarea')])),
                ('editor_theme', models.CharField(default=b'default', max_length=250, choices=[(b'default', b'Default'), (b'ambiance', b'Ambiance'), (b'blackboard', b'Blackboard'), (b'cobalt', b'Cobalt'), (b'eclipse', b'Eclipse'), (b'elegant', b'Elegant'), (b'erlang-dark', b'Erlang Dark'), (b'lesser-dark', b'Lesser Dark'), (b'monokai', b'Monokai'), (b'neat', b'Neat'), (b'night', b'Night'), (b'rubyblue', b'Ruby Blue'), (b'solarized dark', b'Solarized Dark'), (b'solarized light', b'Solarized Light'), (b'twilight', b'Twilight'), (b'vibrant-ink', b'Vibrant Ink'), (b'xq-dark', b'XQ Dark')])),
                ('gittip_username', models.CharField(max_length=250, null=True, blank=True)),
                ('disqus_shortname', models.CharField(max_length=250, null=True, blank=True)),
                ('google_analytics_tracking_id', models.CharField(max_length=250, null=True, blank=True)),
                ('gauges_site_id', models.CharField(max_length=250, null=True, blank=True)),
                ('google_ad_client', models.CharField(max_length=250, null=True, blank=True)),
                ('google_ad_slot', models.CharField(max_length=250, null=True, blank=True)),
                ('google_ad_width', models.CharField(max_length=250, null=True, blank=True)),
                ('google_ad_height', models.CharField(max_length=250, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
