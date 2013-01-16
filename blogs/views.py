from django.shortcuts import get_object_or_404, render_to_response
from annoying.functions import get_object_or_None
from django.template import RequestContext

from snipts.models import Snipt

import datetime

THEME_CHOICES = {
    'D': 'blogs/themes/default/',
    'A': 'blogs/themes/pro-adams/',
}

def blog_list(request, username_or_custom_slug=None):

    if username_or_custom_slug:
        return blog_post(request, username_or_custom_slug)

    snipts = Snipt.objects.filter(user=request.blog_user,
                                  blog_post=True,
                                  public=True,
                                  publish_date__lte=datetime.datetime.now()
                                  ).order_by('-publish_date').exclude(title__iexact='Homepage').exclude(title__iexact='Work')

    normal_snipts = Snipt.objects.filter(blog_post=False, user=request.blog_user, public=True).order_by('-created')
    normal_snipts = normal_snipts.exclude(title__in=[''])
    normal_snipts = normal_snipts.exclude(tags__name__in=['tmp'])
    normal_snipts = normal_snipts[:3]

    sidebar = get_object_or_None(Snipt,
                                 user=request.blog_user,
                                 title='Blog Sidebar')

    context = {
        'blog_user': request.blog_user,
        'has_snipts': True,
        'normal_snipts': normal_snipts,
        'public': True,
        'sidebar': sidebar,
        'snipts': snipts,
    }

    if 'rss' in request.GET:
        context['snipts'] = context['snipts'][:20]
        return rss(request, context)

    if request.blog_user.profile.is_pro:
        template = THEME_CHOICES[request.blog_user.profile.blog_theme]
    else:
        template = THEME_CHOICES['D']

    template = '{}/list.html'.format(template)

    return render_to_response(
            template,
            context,
            context_instance=RequestContext(request)
        )

def blog_post(request, username_or_custom_slug):

    snipt = get_object_or_404(Snipt, user=request.blog_user,
                                     blog_post=True,
                                     public=True,
                                     publish_date__lte=datetime.datetime.now(),
                                     slug=username_or_custom_slug,
                                     )

    sidebar = get_object_or_None(Snipt,
                                 user=request.blog_user,
                                 title='Blog Sidebar')

    normal_snipts = Snipt.objects.filter(blog_post=False, user=request.blog_user, public=True).order_by('-created')
    normal_snipts = normal_snipts.exclude(title__in=[''])
    normal_snipts = normal_snipts.exclude(tags__name__in=['tmp'])
    normal_snipts = normal_snipts[:3]

    if snipt.user != request.user:
        snipt.views = snipt.views + 1
        snipt.save()

    context = {
        'blog_user': request.blog_user,
        'detail': True,
        'has_snipts': True,
        'normal_snipts': normal_snipts,
        'public': True,
        'sidebar': sidebar,
        'snipt': snipt,
    }

    if request.blog_user.profile.is_pro:
        template = THEME_CHOICES[request.blog_user.profile.blog_theme]
    else:
        template = THEME_CHOICES['D']

    template = '{}/post.html'.format(template)

    return render_to_response(
            template,
            context,
            context_instance=RequestContext(request)
        )

def rss(request, context):
    return render_to_response(
            'blogs/themes/default/rss.xml',
            context,
            context_instance=RequestContext(request),
            mimetype="application/rss+xml"
        )
