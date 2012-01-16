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
def list_public(request, tag=None):

    tags = Tag.objects.filter(snipt__public=True)
    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count')[:20]

    snipts = Snipt.objects.filter(public=True).order_by('-created')

    if tag:
        snipts = snipts.filter(tags__name__in=[tag])

    return {
        'snipts': snipts,
        'tags': tags,
        'tag': tag,
    }

@render_to('snipts/list-user.html')
def list_user(request, user, tag=None):

    user = get_object_or_404(User, username=user)
    tags = Tag.objects
    snipts = Snipt.objects

    if user == request.user:
        tags = tags.filter(snipt__user=user)
        snipts = snipts.filter(user=user)
    else:
        tags = tags.filter(snipt__user=user, snipt__public=True)
        snipts = snipts.filter(user=user, public=True)

    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count')
    snipts = snipts.order_by('-created')

    if tag:
        snipts = snipts.filter(tags__name__in=[tag])

    return {
        'snipts': snipts,
        'tags': tags,
        'tag': tag,
        'user': user,
    }

@render_to('snipts/detail.html')
def detail(request, slug):
    return {
        'snipt': slug
    }
