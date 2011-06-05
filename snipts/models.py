from django.contrib.auth.models import User
from django.db import models

from taggit.managers import TaggableManager

class Snipt(models.Model):
    """An individual code snippet."""

    user     = models.ForeignKey(User)

    title    = models.CharField(max_length=255)
    slug     = models.SlugField()
    tags     = TaggableManager()
    old_tags = models.CharField(max_length=255)

    lexer    = models.CharField(max_length=50)
    code     = models.TextField()
    stylized = models.TextField()

    key      = models.CharField(max_length=100)
    public   = models.BooleanField(default=False)
    
    # TODO Set auto_now_add back to True for production!
    created  = models.DateTimeField(auto_now_add=False, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return u'%s' %(self.title)

class Comment(models.Model):
    """A comment on a Snipt"""

    user  = models.ForeignKey(User)
    snipt = models.ForeignKey(Snipt)

    comment = models.TextField()

    # TODO Set auto_now_add back to True for production!
    created  = models.DateTimeField(auto_now_add=False, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
