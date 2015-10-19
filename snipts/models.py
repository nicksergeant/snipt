import datetime
import difflib
import hashlib
import random
import re

from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from markdown_deux import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from snipts.utils import slugify_uniquely
from taggit.managers import TaggableManager
from taggit.utils import edit_string_for_tags
from teams.models import Team


class Snipt(models.Model):
    """An individual Snipt."""

    user = models.ForeignKey(User, blank=True, null=True)
    last_user_saved = models.ForeignKey(User,
                                        blank=True,
                                        null=True,
                                        related_name='last_user_saved')

    title = models.CharField(max_length=255, blank=True, null=True,
                             default='Untitled')
    slug = models.SlugField(max_length=255, blank=True)
    custom_slug = models.SlugField(max_length=255, blank=True)
    tags = TaggableManager()

    lexer = models.CharField(max_length=50)
    code = models.TextField()
    meta = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stylized = models.TextField(blank=True, null=True)
    stylized_min = models.TextField(blank=True, null=True)
    embedded = models.TextField(blank=True, null=True)
    line_count = models.IntegerField(blank=True, null=True, default=None)

    key = models.CharField(max_length=100, blank=True, null=True)
    public = models.BooleanField(default=False)
    blog_post = models.BooleanField(default=False)

    views = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    publish_date = models.DateTimeField(blank=True, null=True)

    def _unidiff_output(self, expected, actual):
        expected = expected.splitlines(1)
        actual = actual.splitlines(1)

        diff = difflib.unified_diff(expected, actual)

        return ''.join(diff)

    def __init__(self, *args, **kwargs):
        super(Snipt, self).__init__(*args, **kwargs)
        self.original_code = self.code

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify_uniquely(self.title, Snipt)

        if not self.key:
            self.key = hashlib.md5(self.slug +
                                   str(datetime.datetime.now()) +
                                   str(random.random())).hexdigest()

        if self.lexer == 'markdown':
            self.stylized = markdown(self.code, 'default')

            # Snipt embeds
            for match in re.findall('\[\[(\w{32})\]\]', self.stylized):
                self.stylized = self.stylized.replace('[[' + str(match) + ']]',
                                                      """
                        <script type="text/javascript"
                                   src="https://snipt.net/embed/{}/?snipt">
                           </script>
                       <div id="snipt-embed-{}"></div>""".format(match, match))

            # YouTube embeds
            for match in re.findall('\[\[youtube-(\w{11})\-(\d+)x(\d+)\]\]',
                                    self.stylized):
                self.stylized = self.stylized \
                    .replace('[[youtube-{}-{}x{}]]'.format(
                        str(match[0]),
                        str(match[1]),
                        str(match[2])),
                        """<iframe width="{}" height="{}"
                           src="https://www.youtube.com/embed/{}"
                           frameborder="0" allowfullscreen></iframe>"""
                        .format(match[1], match[2], match[0]))

            # Vimeo embeds
            for match in re.findall('\[\[vimeo-(\d+)\-(\d+)x(\d+)\]\]',
                                    self.stylized):
                self.stylized = self.stylized \
                    .replace('[[vimeo-{}-{}x{}]]'.format(
                        str(match[0]),
                        str(match[1]),
                        str(match[2])),
                        """<iframe src="https://player.vimeo.com/video/{}"
                           width="{}" height="{}" frameborder="0"
                           webkitAllowFullScreen mozallowfullscreen
                           allowFullScreen></iframe>"""
                        .format(match[0], match[1], match[2]))

            # Tweet embeds
            for match in re.findall('\[\[tweet-(\d+)\]\]', self.stylized):
                self.stylized = self.stylized \
                    .replace(
                        '[[tweet-{}]]'.format(str(match)),
                        '<div class="embedded-tweet" data-tweet-id="{}"></div>'
                        .format(str(match)))

            # Parse Snipt usernames
            for match in re.findall('@(\w+) ', self.stylized):

                # Try and get the Snipt user by username.
                user = get_object_or_None(User, username=match)

                if user:
                    url = user.profile.get_user_profile_url()
                    self.stylized = self.stylized \
                        .replace('@{} '.format(str(match)),
                                 '<a href="{}">@{}</a> '.format(url, match))

        else:
            self.stylized = highlight(self.code,
                                      get_lexer_by_name(self.lexer,
                                                        encoding='UTF-8'),
                                      HtmlFormatter(linenos='table',
                                                    anchorlinenos=True,
                                                    lineanchors='L',
                                                    linespans='L',
                                                    ))
        self.line_count = len(self.code.split('\n'))

        if self.lexer == 'markdown':
            lexer_for_embedded = 'text'
        else:
            lexer_for_embedded = self.lexer

        embedded = highlight(self.code,
                             get_lexer_by_name(lexer_for_embedded,
                                               encoding='UTF-8'),
                             HtmlFormatter(
                                 style='native',
                                 noclasses=True,
                                 prestyles="""
                                     background-color: #1C1C1C;
                                     border-radius: 5px;
                                     color: #D0D0D0;
                                     display: block;
                                     font: 11px Monaco, monospace;
                                     margin: 0;
                                     overflow: auto;
                                     padding: 15px;
                                     -webkit-border-radius: 5px;
                                     -moz-border-radius: 5px;
                                     """))
        embedded = (embedded.replace("\\\"", "\\\\\"")
                            .replace('\'', '\\\'')
                            .replace("\\", "\\\\")
                            .replace('background: #202020', ''))
        self.embedded = embedded

        snipt = super(Snipt, self).save(*args, **kwargs)

        diff = self._unidiff_output(self.original_code or '', self.code)

        if (diff != ''):
            log_entry = SniptLogEntry(user=self.last_user_saved,
                                      snipt=self,
                                      code=self.code,
                                      diff=diff)
            log_entry.save()

        return snipt

    def __unicode__(self):
        return self.title

    def favs(self):
        return Favorite.objects.filter(snipt=self).count()

    def get_stylized_min(self):
        if self.stylized_min is None:
            if self.lexer == 'markdown':
                self.stylized_min = markdown(self.code[:1000], 'default')
            else:
                self.stylized_min = highlight(
                    self.code[:1000],
                    get_lexer_by_name(self.lexer, encoding='UTF-8'),
                    HtmlFormatter(linenos='table',
                                  linenospecial=1,
                                  lineanchors='line'))
        return self.stylized_min

    def get_absolute_url(self):

        if self.blog_post:
            if self.user.profile.blog_domain:
                return u'http://{}/{}/'.format(
                    self.user.profile.blog_domain.split(' ')[0], self.slug)
            else:
                return u'https://{}.snipt.net/{}/'.format(
                    self.user.username.replace('_', '-'), self.slug)

        if self.custom_slug:
            return u'/{}/'.format(self.custom_slug)

        if self.public:
            return u'/{}/{}/'.format(self.user.username, self.slug)
        else:
            return u'/{}/{}/?key={}'.format(
                self.user.username, self.slug, self.key)

    def get_full_absolute_url(self):

        if self.blog_post:
            if self.user.profile.blog_domain:
                return u'http://{}/{}/'.format(
                    self.user.profile.blog_domain.split(' ')[0], self.slug)
            else:
                return u'https://{}.snipt.net/{}/'.format(
                    self.user.username, self.slug)

        if settings.DEBUG:
            root = 'http://local.snipt.net'
        else:
            root = 'https://snipt.net'

        if self.public:
            return u'{}/{}/{}/'.format(root, self.user.username, self.slug)
        else:
            return u'{}/{}/{}/?key={}'.format(root,
                                              self.user.username,
                                              self.slug,
                                              self.key)

    def get_download_url(self):

        try:
            lexer_obj = get_lexer_by_name(self.lexer)
        except ClassNotFound:
            lexer_obj = None

        if lexer_obj and lexer_obj.filenames:
            filename = lexer_obj.filenames[0].replace('*', self.slug)
        else:
            if self.lexer == 'markdown':
                filename = u'{}.md'.format(self.slug)
            else:
                filename = u'{}.txt'.format(self.slug)

        if settings.DEBUG:
            root = 'http://local.snipt.net'
        else:
            root = 'https://snipt.net'

        return u'{}/download/{}/{}'.format(root, self.key, filename)

    def get_embed_url(self):

        if settings.DEBUG:
            root = 'http://local.snipt.net'
        else:
            root = 'https://snipt.net'

        return '{}/embed/{}/'.format(root, self.key)

    def get_raw_url(self):

        if settings.DEBUG:
            root = 'http://local.snipt.net'
        else:
            root = 'https://snipt.net'

        return '{}/raw/{}/'.format(root, self.key)

    @property
    def sorted_tags(self):
        return self.tags.all().order_by('name')

    @property
    def tags_list(self):
        return edit_string_for_tags(self.tags.all())

    @property
    def lexer_name(self):
        if self.lexer == 'markdown':
            return 'Markdown'
        else:
            return get_lexer_by_name(self.lexer).name

    def is_authorized_user(self, user):
        if self.user == user:
            return True
        if self.user.profile.is_a_team:
            team = Team.objects.get(user=self.user, disabled=False)
            return team.user_is_member(user)
        return False


class SniptLogEntry(models.Model):
    """An individual log entry for a Snipt changeset."""

    user = models.ForeignKey(User)
    snipt = models.ForeignKey(Snipt)

    code = models.TextField()
    diff = models.TextField()

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    @property
    def snipt_name(self):
        return self.snipt.title or 'Untitled'


class Favorite(models.Model):
    snipt = models.ForeignKey(Snipt)
    user = models.ForeignKey(User)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return u'{} favorited by {}'.format(self.snipt.title,
                                            self.user.username)
