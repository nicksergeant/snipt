from django.shortcuts import render_to_response
from django.template import RequestContext
from annoying.decorators import render_to

from snipts.models import Snipt


@render_to('blogs/themes/default/homepage.html')
def blog_homepage(request):

    try:
        homepage = Snipt.objects.get(user=request.blog_user, title__iexact='Homepage', blog_post=True, public=True)
    except Snipt.DoesNotExist:
        return blog_list(request)

    context = {
        'homepage': homepage,
        'blog_user': request.blog_user,
    }

    return context

@render_to('blogs/themes/default/list.html')
def blog_list(request):

    snipts = Snipt.objects.filter(user=request.blog_user, blog_post=True, public=True).order_by('-created').exclude(title__iexact='Homepage')

    context = {
        'snipts': snipts,
        'blog_user': request.blog_user,
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
