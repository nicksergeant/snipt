from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user            = models.ForeignKey(User, unique=True)
    is_pro          = models.BooleanField(default=False)
    stripe_id       = models.CharField(max_length=100, null=True, blank=True)

    gittip_username = models.CharField(max_length=250, null=True, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
