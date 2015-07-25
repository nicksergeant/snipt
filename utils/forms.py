from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm


class SniptRegistrationForm(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses and further restricts usernames.
    """
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(
                _("A user with that username already exists."))

        elif '@' in self.cleaned_data['username']:
            raise forms.ValidationError(_("Cannot have '@' in username."))
        elif '.' in self.cleaned_data['username']:
            raise forms.ValidationError(_("Cannot have '.' in username."))
        elif '+' in self.cleaned_data['username']:
            raise forms.ValidationError(_("Cannot have '+' in username."))

        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _("""This email address is already in use. Please supply a
                     different email address."""))
        return self.cleaned_data['email']
