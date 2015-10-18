from annoying.functions import get_object_or_None
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from itertools import chain
from snipts.models import Snipt
from teams.models import Team


class UserProfile(models.Model):

    LIST_VIEW_CHOICES = (
        ('N', 'Normal'),
        ('C', 'Compact'),
    )

    EDITOR_CHOICES = (
        ('C', 'CodeMirror'),
        ('T', 'Textarea'),
    )

    THEME_CHOICES = (
        ('D', 'Default'),
        ('A', 'Pro Adams'),
    )

    EDITOR_THEME_CHOICES = (
        ('default',         'Default'),
        ('ambiance',        'Ambiance'),
        ('blackboard',      'Blackboard'),
        ('cobalt',          'Cobalt'),
        ('eclipse',         'Eclipse'),
        ('elegant',         'Elegant'),
        ('erlang-dark',     'Erlang Dark'),
        ('lesser-dark',     'Lesser Dark'),
        ('monokai',         'Monokai'),
        ('neat',            'Neat'),
        ('night',           'Night'),
        ('rubyblue',        'Ruby Blue'),
        ('solarized dark',  'Solarized Dark'),
        ('solarized light', 'Solarized Light'),
        ('twilight',        'Twilight'),
        ('vibrant-ink',     'Vibrant Ink'),
        ('xq-dark',         'XQ Dark'),
    )

    # User
    user = models.OneToOneField(User)
    is_pro = models.BooleanField(default=False)
    teams_beta_seen = models.BooleanField(default=False)
    teams_beta_applied = models.BooleanField(default=False)
    pro_date = models.DateTimeField(blank=True, null=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    has_gravatar = models.BooleanField(default=False)
    list_view = models.CharField(max_length=1, null=False, blank=False,
                                 default='N', choices=LIST_VIEW_CHOICES)

    # Blog
    blog_title = models.CharField(max_length=250, null=True, blank=True)
    blog_theme = models.CharField(max_length=1, null=False, blank=False,
                                  default='A', choices=THEME_CHOICES)
    blog_domain = models.CharField(max_length=250, null=True, blank=True)

    # Editor
    default_editor = models.CharField(max_length=250, null=False, blank=False,
                                      default='C', choices=EDITOR_CHOICES)
    editor_theme = models.CharField(max_length=250, null=False, blank=False,
                                    default='default',
                                    choices=EDITOR_THEME_CHOICES)

    # Services and Analytics
    gittip_username = models.CharField(max_length=250, null=True, blank=True)
    disqus_shortname = models.CharField(max_length=250, null=True, blank=True)
    google_analytics_tracking_id = models.CharField(max_length=250, null=True,
                                                    blank=True)
    gauges_site_id = models.CharField(max_length=250, null=True, blank=True)

    # Google Ads
    google_ad_client = models.CharField(max_length=250, null=True, blank=True)
    google_ad_slot = models.CharField(max_length=250, null=True, blank=True)
    google_ad_width = models.CharField(max_length=250, null=True, blank=True)
    google_ad_height = models.CharField(max_length=250, null=True, blank=True)

    def get_blog_posts(self):
        return Snipt.objects.filter(user=self.user, blog_post=True,
                                    public=True)

    def get_primary_blog_domain(self):
        if not self.blog_domain:
            return None
        else:
            return self.blog_domain.split(' ')[0]

    def get_user_profile_url(self):

        # If the user has a blog domain, use that.
        if self.blog_domain:
            url = 'http://{}'.format(self.get_primary_blog_domain())

        # Otherwise, if they have blog posts, use their Snipt blog URL.
        elif self.get_blog_posts():
            url = 'https://{}.snipt.net/'.format(self.user.username)

        # Otherwise, use their regular Snipt profile page.
        else:
            url = 'https://snipt.net/{}/'.format(self.user.username)

        return url

    def has_public_snipts(self):
        return True \
            if Snipt.objects.filter(user=self,
                                    public=True).count() > 0 \
            else False

    @property
    def is_a_team(self):
        return True if get_object_or_None(Team, user=self.user) else False

    def teams(self):
        teams_owned = Team.objects.filter(owner=self.user)
        teams_in = Team.objects.filter(members=self.user)
        return list(chain(teams_owned, teams_in))

    def get_account_age(self):
        delta = datetime.now().replace(tzinfo=None) - \
            self.user.date_joined.replace(tzinfo=None)
        return delta.days

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
