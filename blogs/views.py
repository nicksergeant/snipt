from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from snipts.models import Snipt


@render_to('blogs/themes/default/list.html')
def blog_list(request, username_or_custom_slug=None):

    if username_or_custom_slug:
        return blog_post(request, username_or_custom_slug)

    snipts = Snipt.objects.filter(user=request.blog_user, blog_post=True, public=True).order_by('-created').exclude(title__iexact='Homepage')

    sidebar = get_object_or_None(Snipt,
                                 user=request.blog_user,
                                 title='Blog Sidebar')

    context = {
        'blog_user': request.blog_user,
        'has_snipts': True,
        'public': True,
        'sidebar': sidebar,
        'snipts': snipts,
    }

    if 'rss' in request.GET:
        context['snipts'] = context['snipts'][:20]
        return rss(request, context)

    return context

@render_to('blogs/themes/default/post.html')
def blog_post(request, username_or_custom_slug):

    snipt = get_object_or_404(Snipt, user=request.blog_user,
                                     blog_post=True,
                                     public=True,
                                     slug=username_or_custom_slug,
                                     )

    context = {
        'blog_user': request.blog_user,
        'detail': True,
        'has_snipts': True,
        'public': True,
        'snipt': snipt,
    }

    return context

def rss(request, context):
    return render_to_response(
            'rss.xml',
            context,
            context_instance=RequestContext(request),
            mimetype="application/rss+xml"
        )
