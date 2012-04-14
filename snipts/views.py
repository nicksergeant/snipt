from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from pygments.lexers import get_all_lexers
from django.template import RequestContext
from annoying.decorators import render_to
from snipts.models import Favorite, Snipt
from django.db.models import Count
from django.db.models import Q
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
        snipts = snipts.filter(tags__slug__in=[tag_slug])
        tag = get_object_or_404(Tag, slug=tag_slug)
    else:
        tag = None

    context = {
        'has_snipts': True,
        'lexers': sorted(get_all_lexers()),
        'public': True,
        'snipts': snipts,
        'tags': tags,
        'tag': tag,
    }

    if 'rss' in request.GET:
        context['snipts'] = context['snipts'][:20]
        return rss(request, context)

    return context

@render_to('snipts/list-user.html')
def list_user(request, username, tag_slug=None):

    user = get_object_or_404(User, username=username)
    tags = Tag.objects
    snipts = Snipt.objects

    if user == request.user or (request.GET.get('api_key') == user.api_key.key):
        public = False

        favorites = Favorite.objects.filter(user=user).values('snipt')
        favorites = [f['snipt'] for f in favorites]
        snipts = snipts.filter(Q(user=user) | Q(pk__in=favorites))

        tags = tags.filter(Q(snipt__user=user) | Q(snipt__pk__in=favorites))
    else:
        tags = tags.filter(snipt__user=user, snipt__public=True)
        snipts = snipts.filter(user=user, public=True)
        public = True

    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count', 'name')
    snipts = snipts.order_by('-created')

    if tag_slug:
        snipts = snipts.filter(tags__slug__in=[tag_slug])
        tag = get_object_or_404(Tag, slug=tag_slug)
    else:
        tag = None

    context = {
        'has_snipts': True,
        'lexers': sorted(get_all_lexers()),
        'public': public,
        'public_user': (public and user),
        'snipts': snipts,
        'tags': tags,
        'tag': tag,
        'user': user,
    }

    if 'rss' in request.GET:
        context['snipts'] = context['snipts'][:20]
        return rss(request, context)

    return context

@render_to('snipts/detail.html')
def detail(request, username, snipt_slug):

    snipt = get_object_or_404(Snipt, user__username=username, slug=snipt_slug)
    user = snipt.user

    if user != request.user:
        if not snipt.public:
            if 'key' not in request.GET:
                raise Http404
            else:
                if request.GET.get('key') != snipt.key:
                    raise Http404

    tags = Tag.objects

    if user == request.user:
        tags = tags.filter(snipt__user=user)
        public = False
    else:
        tags = tags.filter(snipt__user=user, snipt__public=True)
        public = True

    tags = tags.annotate(count=Count('taggit_taggeditem_items__id'))
    tags = tags.order_by('-count', 'name')

    return {
        'detail': True,
        'has_snipts': True,
        'lexers': sorted(get_all_lexers()),
        'public': public,
        'snipt': snipt,
        'tags': tags,
        'user': user,
    }

def embed(request, snipt_key):
    snipt = get_object_or_404(Snipt, key=snipt_key)

    lines = snipt.embedded.split('\n')
    return render_to_response('snipts/embed.html',
                              {'lines': lines, 'snipt': snipt},
                              context_instance=RequestContext(request),
                              mimetype='application/javascript')

def rss(request, context):
    return render_to_response(
            'rss.xml',
            context,
            context_instance=RequestContext(request),
            mimetype="application/rss+xml"
        )
