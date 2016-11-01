import datetime

from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from snipts.models import Snipt

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
                                  publish_date__lte=datetime.datetime.now()) \
                          .order_by('-publish_date') \
                          .exclude(title__iexact='Homepage') \
                          .exclude(title__iexact='Work')

    normal_snipts = Snipt.objects.filter(blog_post=False,
                                         user=request.blog_user,
                                         public=True) \
                                 .order_by('-created')
    normal_snipts = normal_snipts.exclude(title__in=[''])
    normal_snipts = normal_snipts.exclude(tags__name__in=['tmp'])
    normal_snipts = normal_snipts[:3]

    sidebar = get_object_or_None(Snipt, user=request.blog_user,
                                 title='Sidebar', blog_post=True)
    header = get_object_or_None(Snipt, user=request.blog_user, title='Header',
                                blog_post=True)
    custom_css = get_object_or_None(Snipt, user=request.blog_user, title='CSS',
                                    lexer='css', blog_post=True)

    context = {
        'blog_user': request.blog_user,
        'custom_css': custom_css,
        'has_snipts': True,
        'header': header,
        'normal_snipts': normal_snipts,
        'public': True,
        'sidebar': sidebar,
        'snipts': snipts,
    }

    if 'rss' in request.GET:
        context['snipts'] = context['snipts'][:20]
        return rss(request, context)

    template = THEME_CHOICES[request.blog_user.profile.blog_theme]

    template = '{}/list.html'.format(template)

    return render(
        request,
        template,
        context,
    )


def blog_post(request, username_or_custom_slug):

    snipt = get_object_or_404(Snipt, user=request.blog_user,
                              blog_post=True,
                              public=True,
                              publish_date__lte=datetime.datetime.now(),
                              slug=username_or_custom_slug)

    snipts = Snipt.objects.filter(user=request.blog_user,
                                  blog_post=True,
                                  public=True,
                                  publish_date__lte=datetime.datetime.now()) \
                          .order_by('-publish_date') \
                          .exclude(title__iexact='Homepage') \
                          .exclude(title__iexact='Work')

    sidebar = get_object_or_None(Snipt, user=request.blog_user,
                                 title='Sidebar', blog_post=True)
    header = get_object_or_None(Snipt, user=request.blog_user, title='Header',
                                blog_post=True)
    custom_css = get_object_or_None(Snipt, user=request.blog_user, title='CSS',
                                    lexer='css', blog_post=True)

    normal_snipts = Snipt.objects.filter(blog_post=False,
                                         user=request.blog_user,
                                         public=True).order_by('-created')
    normal_snipts = normal_snipts.exclude(title__in=[''])
    normal_snipts = normal_snipts.exclude(tags__name__in=['tmp'])
    normal_snipts = normal_snipts[:3]

    if snipt.user != request.user:
        snipt.views = snipt.views + 1
        snipt.save()

    context = {
        'blog_user': request.blog_user,
        'custom_css': custom_css,
        'detail': True,
        'has_snipts': True,
        'header': header,
        'normal_snipts': normal_snipts,
        'public': True,
        'sidebar': sidebar,
        'snipt': snipt,
        'snipts': snipts,
    }

    template = THEME_CHOICES[request.blog_user.profile.blog_theme]

    template = '{}/post.html'.format(template)

    return render(request, template, context)


def rss(request, context):
    return render(request, 'blogs/themes/default/rss.xml', context,
                  content_type="application/rss+xml")
