from taggit.utils import edit_string_for_tags, parse_tags
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.template.defaultfilters import date, urlize, linebreaksbr
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from tastypie.validation import Validation
from tastypie.models import create_api_key
from snipts.models import Favorite, Snipt
from haystack.query import SearchQuerySet
from accounts.models import UserProfile
from tastypie.cache import SimpleCache
from tastypie.fields import ListField
from taggit.models import Tag
from django.db import models
from tastypie import fields

import datetime, hashlib, time, re

import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc

models.signals.post_save.connect(create_api_key, sender=User)


class FavoriteValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        snipt = bundle.data['snipt']

        if Favorite.objects.filter(user=request.user, snipt=snipt).count():
            errors['duplicate'] = 'User has already favorited this snipt.'

        return errors

class UserProfileValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        for field in bundle.data:
            if not re.match('^[ A-Za-z0-9\/\@\._-]*$', bundle.data[field]):
                errors[field] = 'Only spaces, letters, numbers, underscores, dashes, periods, forward slashes, and "at sign" are valid.'

        return errors


class PublicUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username',]
        include_absolute_url = True
        allowed_methods = ['get']
        filtering = { 'username': 'exact', }
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['snipts'] = '/api/public/snipt/?user=%d' % bundle.obj.id
        return bundle

class PublicTagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.filter(snipt__public=True)
        queryset = queryset.annotate(count=models.Count('taggit_taggeditem_items__id'))
        queryset = queryset.order_by('-count', 'name')
        resource_name = 'tag'
        fields = ['id', 'name',]
        allowed_methods = ['get']
        max_limit = 200
        cache = SimpleCache()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(PublicTagResource, self).build_filters(filters)

        if 'q' in filters:
            orm_filters['slug'] = filters['q']

        return orm_filters

    def dehydrate(self, bundle):
        bundle.data['absolute_url'] = '/public/tag/%s/' % bundle.obj.slug
        bundle.data['snipts'] = '/api/public/snipt/?tag=%d' % bundle.obj.id
        bundle.data['count'] = bundle.obj.taggit_taggeditem_items.filter(
                               snipt__public=True).count()
        return bundle

class PublicSniptResource(ModelResource):
    user = fields.ForeignKey(PublicUserResource, 'user', full=True)
    tags = fields.ToManyField(PublicTagResource, 'tags', related_name='tag', full=True)

    class Meta:
        queryset = Snipt.objects.filter(public=True).order_by('-created')
        resource_name = 'snipt'
        fields = ['id', 'title', 'slug', 'lexer', 'code', 'description', 'line_count',
                  'stylized', 'created', 'modified',]
        include_absolute_url = True
        allowed_methods = ['get']
        filtering = { 'user': 'exact', }
        ordering = ['created', 'modified',]
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['embed_url'] = bundle.obj.get_embed_url()
        bundle.data['full_absolute_url'] = bundle.obj.get_full_absolute_url()
        bundle.data['description_rendered'] = linebreaksbr(urlize(bundle.obj.description))
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(PublicSniptResource, self).build_filters(filters)

        if 'tag' in filters:
            tag = Tag.objects.get(pk=filters['tag'])
            tagged_items = tag.taggit_taggeditem_items.all()
            orm_filters['pk__in'] = [i.object_id for i in tagged_items]

        if 'q' in filters:
            sqs = SearchQuerySet().auto_query(filters['q'])
            orm_filters['pk__in'] = [i.pk for i in sqs]

        return orm_filters


class PrivateUserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        excludes = ['is_pro', 'stripe_id']
        validation = UserProfileValidation()
        include_absolute_url = False
        allowed_methods = ['get', 'put']
        list_allowed_methods = []
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        max_limit = 200

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def dehydrate(self, bundle):
        bundle.data['email'] = bundle.obj.user.email
        bundle.data['username'] = bundle.obj.user.username
        bundle.data['user_id'] = bundle.obj.user.id
        bundle.data['api_key'] = bundle.obj.user.api_key.key
        bundle.data['is_pro'] = bundle.obj.user.profile.is_pro
        return bundle

class PrivateUserResource(ModelResource):
    profile = fields.ForeignKey(PrivateUserProfileResource, 'profile', full=False)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username', 'email']
        include_absolute_url = True
        allowed_methods = ['get']
        list_allowed_methods = []
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        max_limit = 200
        cache = SimpleCache()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(username=request.user.username)

    def dehydrate(self, bundle):
        bundle.data['email_md5'] = hashlib.md5(bundle.obj.email.lower()).hexdigest()
        return bundle

class PrivateTagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        fields = ['id', 'name',]
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        max_limit = 200
        cache = SimpleCache()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(PrivateTagResource, self).build_filters(filters)

        if 'q' in filters:
            orm_filters['slug'] = filters['q']

        return orm_filters
    def dehydrate(self, bundle):
        bundle.data['absolute_url'] = '/%s/tag/%s/' % (bundle.request.user.username,
                                                       bundle.obj.slug)
        bundle.data['snipts'] = '/api/private/snipt/?tag=%d' % bundle.obj.id

        bundle.data['count'] = bundle.obj.taggit_taggeditem_items.filter(
                                       snipt__user=bundle.request.user
                                   ).count()

        return bundle

    def apply_authorization_limits(self, request, object_list):
        object_list = object_list.filter(snipt__user=request.user)
        object_list = object_list.annotate(count=models.Count('taggit_taggeditem_items__id'))
        object_list = object_list.order_by('-count', 'name')
        return object_list

class PrivateSniptResource(ModelResource):
    user = fields.ForeignKey(PrivateUserResource, 'user', full=True)
    tags = fields.ToManyField(PrivateTagResource, 'tags', related_name='tag', full=True)
    tags_list = ListField()

    class Meta:
        queryset = Snipt.objects.all().order_by('-created')
        resource_name = 'snipt'
        fields = ['id', 'title', 'slug', 'lexer', 'code', 'description', 'line_count', 'stylized',
                  'key', 'public', 'blog_post', 'created', 'modified', 'publish_date',]
        include_absolute_url = True
        detail_allowed_methods = ['get', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        ordering = ['created', 'modified',]
        always_return_data = True
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['embed_url'] = bundle.obj.get_embed_url()
        bundle.data['tags_list'] = edit_string_for_tags(bundle.obj.tags.all())
        bundle.data['full_absolute_url'] = bundle.obj.get_full_absolute_url()
        bundle.data['description_rendered'] = linebreaksbr(urlize(bundle.obj.description))

        if bundle.data['user'].data['profile']['is_pro']:
            bundle.data['views'] = bundle.obj.views
            bundle.data['favs'] = bundle.obj.favs()

        if bundle.data['publish_date']:
            bundle.data['publish_date'] = date(bundle.data['publish_date'], 'M d, Y \\a\\t h:i A')

        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['tags_list'] = bundle.data.get('tags')
        bundle.data['tags'] = ''

        if 'blog_post' in bundle.data:
            bundle = self._clean_publish_date(bundle)

        return super(PrivateSniptResource, self).obj_create(bundle, request,
                     user=request.user, **kwargs)

    def obj_update(self, bundle, request=None, **kwargs):
        bundle.data['user'] = request.user

        if type(bundle.data['tags']) in (str, unicode):
            bundle.data['tags_list'] = bundle.data['tags']
        else:
            bundle.data['tags_list'] = ''
        bundle.data['tags'] = ''

        if 'blog_post' in bundle.data:
            bundle = self._clean_publish_date(bundle)

        return super(PrivateSniptResource, self).obj_update(bundle, request,
                     user=request.user, **kwargs)

    def _clean_publish_date(self, bundle):
        if bundle.data['blog_post'] and 'publish_date' not in bundle.data:
            bundle.data['publish_date'] = datetime.datetime.now()
        elif bundle.data['publish_date'] == '':
            bundle.data['publish_date'] = datetime.datetime.now()
        elif bundle.data['blog_post']:
            c = pdc.Constants()
            p = pdt.Calendar(c)
            publish_date, result = p.parse(bundle.data['publish_date'])

            if result != 0:
                publish_date = time.strftime("%Y-%m-%d %H:%M:%S", publish_date)
            else:
                publish_date = datetime.datetime.now()

            bundle.data['publish_date'] = publish_date
        elif not bundle.data['blog_post']:
            bundle.data['publish_date'] = None

        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(PrivateSniptResource, self).build_filters(filters)

        if 'tag' in filters:
            tag = Tag.objects.get(pk=filters['tag'])
            tagged_items = tag.taggit_taggeditem_items.all()
            orm_filters['pk__in'] = [i.object_id for i in tagged_items]

        if 'q' in filters:
            sqs = SearchQuerySet().auto_query(filters['q'])
            orm_filters['pk__in'] = [i.pk for i in sqs]

        return orm_filters

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def save_m2m(self, bundle):
        tags = bundle.data.get('tags_list', [])
        if tags != '':
            bundle.obj.tags.set(*parse_tags(tags))
        else:
            bundle.obj.tags.set()

class PrivateFavoriteResource(ModelResource):
    user = fields.ForeignKey(PrivateUserResource, 'user', full=True)
    snipt = fields.ForeignKey(PrivateSniptResource, 'snipt', full=False)

    class Meta:
        queryset = Favorite.objects.all().order_by('-created')
        resource_name = 'favorite'
        fields = ['id',]
        validation = FavoriteValidation()
        detail_allowed_methods = ['get', 'post', 'delete']
        list_allowed_methods = ['get', 'post',]
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        ordering = ['created',]
        always_return_data = True
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['snipt'] = '/api/public/snipt/{}/'.format(
                bundle.obj.snipt.pk)
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['user'] = request.user
        bundle.data['snipt'] = Snipt.objects.get(pk=bundle.data['snipt'])
        return super(PrivateFavoriteResource, self).obj_create(bundle, request,
                     user=request.user, **kwargs)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
