from django.conf import settings
from django.core.management.base import BaseCommand
from jobs.models import Job

import json
import requests


class Command(BaseCommand):
    help = 'Import jobs'
    listings = []

    def get_for_page(self, page):
        r = requests.get('{}&page={}'.format(settings.JOBS_BASE_URL, page))
        obj = r.json()
        self.listings.extend(obj['listings']['listing'])

        if page < obj['listings']['pages']:
            return self.get_for_page(page + 1)

        return self.listings

    def handle(self, *args, **options):
        listings = self.get_for_page(1)

        jobs = Job.objects.all()
        for job in jobs:
            job.delete()

        for listing in listings:

            try:
                location = listing['company']['location']['city']
            except:
                location = ''

            try:
                company = str(listing['company']['name'])
            except:
                company = ''

            newjob = Job(title=listing['title'],
                         company=company,
                         location=location,
                         url=listing['url'],
                         data=json.dumps(listing),
                         created=listing['post_date'])
            newjob.save()
