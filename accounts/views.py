from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from annoying.decorators import render_to
from accounts.forms import AccountForm
from django.contrib import messages
from snipts.models import Snipt

@login_required
@render_to('account.html')
def account(request):

    if request.POST:
        form = AccountForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.add_message(request, 25, 'Account settings saved.')
            return HttpResponseRedirect('/account/')

    else:
        profile = request.user.profile

        form = AccountForm(initial={
            'gittip_username': profile.gittip_username,
            'blog_title': profile.blog_title,
            'blog_theme': profile.blog_theme,
            'blog_domain': profile.blog_domain
        })

    return {
        'form': form
    }

@login_required
@render_to('stats.html')
def stats(request):

    if not request.user.profile.is_pro:
        return HttpResponseRedirect('/pro/')

    snipts = Snipt.objects.filter(user=request.user).order_by('-views')

    return {
        'snipts': snipts
    }
