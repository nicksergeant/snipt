from snipts.api import PublicSniptResource, PublicTagResource
from annoying.decorators import render_to
from django.db.models import Count
from snipts.models import Snipt
from taggit.models import Tag

@render_to('home.html')
def home(request):

    if request.user.is_authenticated():
        return home_user(request)

    tags = Tag.objects.filter(snipt__public=True)
    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count')[:20]

    snipts = Snipt.objects.filter(public=True).order_by('-created')

    return {
        'snipts': snipts,
        'tags': tags,
    }

@render_to('home.html')
def home_user(request):

    tags = Tag.objects.filter(snipt__user=request.user)
    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count')[:20]

    snipts = Snipt.objects.filter(public=True).order_by('-created')

    return {
        'snipts': snipts,
        'tags': tags,
    }
