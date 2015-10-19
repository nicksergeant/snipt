from django.contrib.auth.models import User
from django.db import models
from snipts.utils import slugify_uniquely


class Team(models.Model):

    PLANS = (
        ('snipt-teams-25-monthly', '25 users, monthly'),
        ('snipt-teams-100-monthly', '100 users, monthly'),
        ('snipt-teams-250-monthly', '250 users, monthly'),
        ('snipt-teams-unlimited-monthly', 'Unlimited users, monthly'),
        ('snipt-teams-25-yearly', '25 users, yearly'),
        ('snipt-teams-100-yearly', '100 users, yearly'),
        ('snipt-teams-250-yearly', '250 users, yearly'),
        ('snipt-teams-unlimited-yearly', 'Unlimited users, yearly'),
    )

    email = models.EmailField(max_length=255)
    members = models.ManyToManyField(User, related_name='member', blank=True)
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='owner')
    slug = models.SlugField(max_length=255, blank=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, blank=True, null=True)
    plan = models.CharField(max_length=100, default='snipt-teams-25-monthly',
                            choices=PLANS, blank=True, null=True)
    disabled = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, User, 'username')
        return super(Team, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.all().count() + 1

    @property
    def member_limit(self):

        if self.disabled:
            return 0

        plan_map = {
            'snipt-teams-25-monthly': 25,
            'snipt-teams-100-monthly': 100,
            'snipt-teams-250-monthly': 250,
            'snipt-teams-unlimited-monthly': float('inf'),
            'snipt-teams-25-yearly': 25,
            'snipt-teams-100-yearly': 100,
            'snipt-teams-250-yearly': 250,
            'snipt-teams-unlimited-yearly': float('inf')
        }

        if plan_map[self.plan] == float('inf'):
            return 'Unlimited'
        else:
            return plan_map[self.plan]

    def user_is_member(self, user):
        if self.disabled:
            return False
        if self.owner == user or user in self.members.all():
            return True
        return False
