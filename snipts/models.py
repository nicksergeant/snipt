from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models

from taggit.managers import TaggableManager

class Snipt(models.Model):
    """An individual Snipt."""

    user     = models.ForeignKey(User)

    title    = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug     = models.SlugField(max_length=255, blank=True)
    tags     = TaggableManager()

    lexer    = models.CharField(max_length=50)
    code     = models.TextField()
    stylized = models.TextField()

    key      = models.CharField(max_length=100)
    public   = models.BooleanField(default=False)
    
    # TODO Set auto_now_add back to True for production!
    created  = models.DateTimeField(auto_now_add=False, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(Snipt, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "https://snipt.net/%s/%s/" % (self.user.username, self.slug)

class Comment(models.Model):
    """A comment on a Snipt"""

    user  = models.ForeignKey(User)
    snipt = models.ForeignKey(Snipt)

    comment = models.TextField()

    # TODO Set auto_now_add back to True for production!
    created  = models.DateTimeField(auto_now_add=False, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return u'%s on %s' %(self.user, self.snipt)
