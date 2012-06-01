from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from annoying.decorators import render_to

from snipts.models import Snipt


@render_to('blogs/list.html')
def list_blog(request, subdomain):

    subdomain = subdomain.replace('-', '_')
    user = get_object_or_404(User, username__iexact=subdomain)
    snipts = Snipt.objects.filter(user=user, blog_post=True, public=True).order_by('-created')

    context = {
        'snipts': snipts,
        'user': user,
    }

    if 'rss' in request.GET:
        context['snipts'] = context['snipts'][:20]
        return rss(request, context)

    return context

def rss(request, context):
    return render_to_response(
            'rss.xml',
            context,
            context_instance=RequestContext(request),
            mimetype="application/rss+xml"
        )
