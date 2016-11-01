from registration.backends.default.views import RegistrationView
from utils.forms import SniptRegistrationForm


class SniptRegistrationView(RegistrationView):
    """
    Custom registration view that uses our custom form.
    """
    form_class = SniptRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, request):
        return '/account/activate/'
