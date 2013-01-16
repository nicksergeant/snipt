from django.forms import ModelForm
from accounts.models import UserProfile

class AccountForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'is_pro', 'stripe_id',)
