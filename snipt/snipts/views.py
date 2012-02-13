from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from annoying.decorators import render_to
from django.db.models import Count
from snipts.models import Snipt
from taggit.models import Tag

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/%s/' % request.user.username)
    else:
        return list_public(request)

@render_to('snipts/list-public.html')
def list_public(request, tag_slug=None):

    tags = Tag.objects.filter(snipt__public=True)
    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count', 'name')[:20]

    snipts = Snipt.objects.filter(public=True).order_by('-created')

    if tag_slug:
        snipts = snipts.filter(tags__name__in=[tag_slug])

    return {
        'public': True,
        'snipts': snipts,
        'tags': tags,
        'tag': tag_slug,
    }

@render_to('snipts/list-user.html')
def list_user(request, username, tag_slug=None):

    user = get_object_or_404(User, username=username)
    tags = Tag.objects
    snipts = Snipt.objects

    if user == request.user:
        tags = tags.filter(snipt__user=user)
        snipts = snipts.filter(user=user)
    else:
        tags = tags.filter(snipt__user=user, snipt__public=True)
        snipts = snipts.filter(user=user, public=True)

    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count', 'name')
    snipts = snipts.order_by('-created')

    if tag_slug:
        snipts = snipts.filter(tags__name__in=[tag_slug])

    return {
        'snipts': snipts,
        'tags': tags,
        'tag': tag_slug,
        'user': user,
    }

@render_to('snipts/detail.html')
def detail(request, username, snipt_slug):

    snipt = get_object_or_404(Snipt, user__username=username, slug=snipt_slug)
    user = snipt.user
    tags = Tag.objects

    if user == request.user:
        tags = tags.filter(snipt__user=user)
    else:
        tags = tags.filter(snipt__user=user, snipt__public=True)

    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count', 'name')

    return {
        'snipt': snipt,
        'user': user,
        'tags': tags,
    }
