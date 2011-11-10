from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

from taggit.managers import TaggableManager

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


site = Site.objects.all()[0]

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
    line_count = models.IntegerField(blank=True, null=True, default=None)

    key      = models.CharField(max_length=100)
    public   = models.BooleanField(default=False)
    
    # TODO Set back to True for production!
    created  = models.DateTimeField(auto_now_add=False, editable=False)
    modified = models.DateTimeField(auto_now=False, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(Snipt, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/" % (self.user.username, self.slug)

    #TODO This needs to be deprecated - render stylized version on save
    def get_stylized(self):
        if self.stylized == '':
            self.stylized = highlight(self.code,
                                      get_lexer_by_name(self.lexer, encoding='UTF-8'),
                                      HtmlFormatter())
            self.save()
            return self.stylized
        else:
            return self.stylized

    #TODO This needs to be deprecated - render line count on save
    def get_line_count(self):
        if not self.line_count:
            self.line_count = len(self.code.split('\n'))
            self.save()
            return self.line_count
        else:
            return self.line_count

    def get_embed_url(self):
        return 'http%s://%s/embed/%s/' % ('s' if settings.USE_HTTPS else '',
                                          site.domain,
                                          self.key)

    @property
    def sorted_tags(self):
        return self.tags.all().order_by('name')

    @property
    def lexer_name(self):
        return get_lexer_by_name(self.lexer).name

class Comment(models.Model):
    """A comment on a Snipt"""

    user  = models.ForeignKey(User)
    snipt = models.ForeignKey(Snipt)

    comment = models.TextField()

    # TODO Set back to True for production!
    created  = models.DateTimeField(auto_now_add=False, editable=False)
    modified = models.DateTimeField(auto_now=False, editable=False)

    def __unicode__(self):
        return u'%s on %s' %(self.user, self.snipt)

    def get_absolute_url(self):
        return '%s#comment-%d' % (self.snipt.get_absolute_url(), self.id)
