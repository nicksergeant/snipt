from django.contrib.auth.models import User
from django.db import models

import caching.base


class UserProfile(caching.base.CachingMixin, models.Model):
    user   = models.ForeignKey(User, unique=True)
    is_pro = models.BooleanField(default=False)

    objects = caching.base.CachingManager()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
