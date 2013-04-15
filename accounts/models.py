from django.contrib.auth.models import User
from django.db import models
from snipts.models import Snipt

class UserProfile(models.Model):

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
    user            = models.ForeignKey(User, unique=True)
    is_pro          = models.BooleanField(default=False)
    stripe_id       = models.CharField(max_length=100, null=True, blank=True)
    has_gravatar    = models.BooleanField(default=False)

    # Blog
    blog_title      = models.CharField(max_length=250, null=True, blank=True)
    blog_theme      = models.CharField(max_length=1,   null=False, blank=False, default='D', choices=THEME_CHOICES)
    blog_domain     = models.CharField(max_length=250, null=True, blank=True)

    # Editor
    default_editor  = models.CharField(max_length=250, null=False, blank=False, default='C', choices=EDITOR_CHOICES)
    editor_theme    = models.CharField(max_length=250, null=False, blank=False, default='default', choices=EDITOR_THEME_CHOICES)

    # Services and Analytics
    gittip_username  = models.CharField(max_length=250, null=True, blank=True)
    disqus_shortname = models.CharField(max_length=250, null=True, blank=True)
    google_analytics_tracking_id = models.CharField(max_length=250, null=True, blank=True)
    gauges_site_id   = models.CharField(max_length=250, null=True, blank=True)

    # Google Ads
    google_ad_client = models.CharField(max_length=250, null=True, blank=True)
    google_ad_slot   = models.CharField(max_length=250, null=True, blank=True)
    google_ad_width  = models.CharField(max_length=250, null=True, blank=True)
    google_ad_height = models.CharField(max_length=250, null=True, blank=True)

    def get_blog_posts(self):
        return Snipt.objects.filter(user=self.user, blog_post=True, public=True)

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


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
