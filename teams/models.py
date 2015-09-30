from django.contrib.auth.models import User
from django.db import models
from snipts.utils import slugify_uniquely


class Team(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    owner = models.ForeignKey(User, related_name='owner')
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    members = models.ManyToManyField(User, related_name='member', blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, User, 'username')
        return super(Team, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
