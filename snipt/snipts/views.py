from snipts.api import PublicSniptResource, PublicTagResource
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from annoying.decorators import render_to
from django.db.models import Count
from snipts.models import Snipt
from taggit.models import Tag

TODO: MUST UPGRADE TASTYPIE.

def home(request):
    if request.user.is_authenticated():
        return list_user(request, user=request.user)
    else:
        return list_public(request)

@render_to('snipts/list-public.html')
def list_public(request):

    tags = Tag.objects.filter(snipt__public=True)
    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count')[:20]

    snipts = Snipt.objects.filter(public=True).order_by('-created')

    return {
        'snipts': snipts,
        'tags': tags,
    }

@render_to('snipts/list-user.html')
def list_user(request, user):

    if type(user) == unicode:
        user = get_object_or_404(User, username=user.strip('/'))

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

    return {
        'snipts': snipts,
        'tags': tags,
        'user': user,
    }
