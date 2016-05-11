from django.contrib.auth.forms import AuthenticationForm


class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
