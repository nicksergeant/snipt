from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from annoying.decorators import render_to
from snipts.models import Snipt

@login_required
@render_to('account.html')
def account(request):
    return {}

@login_required
@render_to('stats.html')
def stats(request):

    if not request.user.profile.is_pro:
        return HttpResponseRedirect('/pro/')

    snipts = Snipt.objects.filter(user=request.user).order_by('-views')

    return {
        'snipts': snipts
    }
