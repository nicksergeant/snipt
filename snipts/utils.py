import uuid

from django.contrib.auth import authenticate, login
from django.template.defaultfilters import slugify
from pygments.lexers import get_all_lexers
from registration.signals import user_registered


def slugify_uniquely(value, model, slugfield="slug"):
    suffix = False
    potential = base = slugify(value)[:255]

    while True:
        if suffix:
            if value:
                potential = "-".join([base, str(suffix)])
            else:
                potential = str(suffix)
        if not model.objects.filter(**{slugfield: potential}).count():
            return potential
        suffix = str(uuid.uuid4()).split('-')[0]


def activate_user(user, request, **kwargs):
    user.is_active = True
    user.save()

    user = authenticate(username=request.POST['username'],
                        password=request.POST['password1'])
    login(request, user)


def get_lexers_list():
    lexers = list(get_all_lexers())

    for l in lexers:
        if l[0] == 'ANTLR With Java Target':
            lexers.remove(l)

    lexers.append(('Markdown', ('markdown',),))
    lexers = sorted(lexers)

    return lexers

user_registered.connect(activate_user)
