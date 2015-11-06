from registration.backends.default.views import RegistrationView
from utils.forms import SniptRegistrationForm


class SniptRegistrationView(RegistrationView):
    """
    Custom registration view that uses our custom form.
    """
    form_class = SniptRegistrationForm

    def get_success_url(self, request, user):
        return '/{}/'.format(user.username)
