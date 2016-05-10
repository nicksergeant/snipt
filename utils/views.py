import requests

from django.conf import settings
from django.http import HttpResponse
from registration.backends.default.views import ActivationView, RegistrationView
from utils.forms import SniptRegistrationForm


class SniptRegistrationView(RegistrationView):
    """
    Custom registration view that uses our custom form.
    """
    form_class = SniptRegistrationForm

    def dispatch(self, request, *args, **kwargs):

        if request.method == 'POST':
            payload = {
                'secret': settings.RECAPTCHA_SECRET,
                'response': request.POST['g-recaptcha-response'],
                'remoteip': request.META.get('REMOTE_ADDR')
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                              data=payload)

            if not r.json()['success']:
                return HttpResponse('You failed the robot check. Go back and try again.')

        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, request, user):
        return '/{}/'.format(user.username)
