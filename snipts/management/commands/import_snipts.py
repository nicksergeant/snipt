#!/usr/bin/env python

from snipts.models import Snipt
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

import requests


def get_snipts(api_key, from_username, url=None, snipts=[]):
    path = url or '/api/private/snipt/?limit=50&api_key={}&username={}&format=json'.format(api_key, from_username)
    res = requests.get('https://snipt.net' + path)
    json = res.json()

    print(u"Fetched snipts {} through {} of {}".format(
        json["meta"]["offset"],
        json["meta"]["offset"] + json["meta"]["limit"],
        json["meta"]["total_count"]
    ))

    snipts.extend(json["objects"])

    if json["meta"]["next"]:
        return get_snipts(api_key, from_username, json["meta"]["next"], snipts)
    else:
        return snipts


class Command(BaseCommand):
    help = u"Import snipts from snipt.net."

    def add_arguments(self, parser):
        parser.add_argument('api_key', nargs='+', type=str)
        parser.add_argument('from_username', nargs='+', type=str)
        parser.add_argument('to_username', nargs='+', type=str)

    def handle(self, *args, **options):
        api_key = options['api_key'][0]
        from_username = options['from_username'][0]
        to_username = options['to_username'][0]
        to_user = User.objects.get(username=to_username)

        print(u"Fetching snipts...")

        items = get_snipts(api_key, from_username)

        for snipt in items:
            s = Snipt(
                blog_post=snipt["blog_post"],
                code=snipt["code"],
                created=snipt["created"],
                description=snipt["description"],
                id=snipt["id"],
                key=snipt["key"],
                lexer=snipt["lexer"],
                line_count=snipt["line_count"],
                meta=snipt["meta"],
                modified=snipt["modified"],
                public=snipt["public"],
                publish_date=snipt["publish_datetime"],
                secure=snipt["secure"],
                slug=snipt["slug"],
                stylized=snipt["stylized"],
                title=snipt["title"],
                user=to_user,
                views=snipt["views"]
            )

            for tag in snipt["tags"]:
                s.tags.add(tag["name"])

            s.save()

            self.stdout.write(snipt["title"])
