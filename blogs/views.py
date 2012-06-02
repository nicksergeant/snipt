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
        'blog_user': request.blog_user,
        'homepage': homepage,
        'public': True,
    }

    return context

@render_to('blogs/themes/default/list.html')
def blog_list(request, username_or_custom_slug=None):

    if username_or_custom_slug and username_or_custom_slug != 'blog':
        return blog_post(request, username_or_custom_slug)

    snipts = Snipt.objects.filter(user=request.blog_user, blog_post=True, public=True).order_by('-created').exclude(title__iexact='Homepage')

    context = {
        'blog_user': request.blog_user,
        'has_snipts': True,
        'public': True,
        'snipts': snipts,
    }

    if 'rss' in request.GET:
        context['snipts'] = context['snipts'][:20]
        return rss(request, context)

    return context

@render_to('blogs/themes/default/list.html')
def blog_post(request, username_or_custom_slug):

    snipts = Snipt.objects.filter(user=request.blog_user,
                                  blog_post=True,
                                  public=True,
                                  slug=username_or_custom_slug,
                                  ).order_by('-created').exclude(title__iexact='Homepage')

    context = {
        'blog_user': request.blog_user,
        'detail': True,
        'has_snipts': True,
        'public': True,
        'snipts': snipts,
    }

    return context

def rss(request, context):
    return render_to_response(
            'rss.xml',
            context,
            context_instance=RequestContext(request),
            mimetype="application/rss+xml"
        )
