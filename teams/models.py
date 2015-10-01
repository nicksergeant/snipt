from django.contrib.auth.models import User
from django.db import models
from snipts.utils import slugify_uniquely


class Team(models.Model):
    email = models.EmailField(max_length=255)
    members = models.ManyToManyField(User, related_name='member', blank=True)
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='owner')
    slug = models.SlugField(max_length=255, blank=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, User, 'username')
        return super(Team, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
