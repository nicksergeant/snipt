from django import forms
from accounts.models import UserProfile

import re

class AccountForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'is_pro', 'stripe_id',)

    def clean_blog_title(self):
        data = self.cleaned_data['blog_title']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_blog_theme(self):
        data = self.cleaned_data['blog_theme']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_blog_domain(self):
        data = self.cleaned_data['blog_domain']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_default_editor(self):
        data = self.cleaned_data['default_editor']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_editor_theme(self):
        data = self.cleaned_data['editor_theme']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_gittip_username(self):
        data = self.cleaned_data['gittip_username']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_disqus_shortname(self):
        data = self.cleaned_data['disqus_shortname']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_google_analytics_tracking_id(self):
        data = self.cleaned_data['google_analytics_tracking_id']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_gauges_site_id(self):
        data = self.cleaned_data['gauges_site_id']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_google_ad_client(self):
        data = self.cleaned_data['google_ad_client']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_google_ad_slot(self):
        data = self.cleaned_data['google_ad_slot']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_google_ad_width(self):
        data = self.cleaned_data['google_ad_width']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

    def clean_google_ad_height(self):
        data = self.cleaned_data['google_ad_height']

        if not re.match('^[A-Za-z0-9\._-]*$', data):
            raise forms.ValidationError('Only letters, numbers, underscores, dashes, and periods are valid.')

        return data

