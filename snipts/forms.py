from django.forms import ModelForm
from snipts.models import Snipt


class SniptForm(ModelForm):
    class Meta:
        model = Snipt
