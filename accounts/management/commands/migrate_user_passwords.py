#!/usr/bin/env python

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = u"Convert user passwords to use built-in Django bcrypt."

    def handle(self, *args, **options):

        users = User.objects.all()

        self.stdout.write(u"Updating %s user passwords..." % users.count())

        for user in users:
            if user.password[0:3] == "bc$":
                pw = user.password
                new_password = pw[0:3].replace("bc$", "bcrypt$") + pw[3:]
                user.password = new_password
                user.save()

        self.stdout.write(u"User passwords migrated successfully.")
