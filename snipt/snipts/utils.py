from django.contrib.auth import authenticate, login
from django.template.defaultfilters import slugify
from registration.signals import user_registered


def slugify_uniquely(value, model, slugfield="slug"):
    suffix = 0
    potential = base = slugify(value)[:255]

    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).count():
            return potential
        suffix += 1

def activate_user(user, request, **kwargs):
    user.is_active = True
    user.save()

    user = authenticate(username=request.POST['username'],
                        password=request.POST['password1'])
    login(request, user)


user_registered.connect(activate_user)
