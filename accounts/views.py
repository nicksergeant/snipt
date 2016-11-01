from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from snipts.models import Snipt


@login_required
@render_to('account.html')
def account(request):
    return {}


@login_required
@render_to('activate.html')
def activate(request):
    request.user.is_active = True
    request.user.save()
    return HttpResponseRedirect('/login-redirect/')


@login_required
@render_to('stats.html')
def stats(request):

    snipts = Snipt.objects.filter(user=request.user).order_by('-views')

    return {
        'snipts': snipts
    }
