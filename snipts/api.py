from taggit.utils import edit_string_for_tags, parse_tags
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.template.defaultfilters import date
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from tastypie.validation import Validation
from tastypie.models import create_api_key
from snipts.models import Favorite, Snipt
from haystack.query import SearchQuerySet
from tastypie.cache import SimpleCache
from tastypie.fields import ListField
from taggit.models import Tag
from django.db import models
from tastypie import fields

import datetime, hashlib, time

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


class PublicUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username',]
        include_absolute_url = True
        allowed_methods = ['get']
        list_allowed_methods = []
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
        cache = SimpleCache()

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
        fields = ['id', 'title', 'slug', 'lexer', 'code', 'line_count',
                  'stylized', 'created', 'modified',]
        include_absolute_url = True
        allowed_methods = ['get']
        filtering = { 'user': 'exact', }
        ordering = ['created', 'modified',]
        # TODO max_limit does not work.
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['embed_url'] = bundle.obj.get_embed_url()
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


class PrivateUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username', 'email',]
        include_absolute_url = True
        allowed_methods = ['get']
        list_allowed_methods = []
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
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
        cache = SimpleCache()

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
        fields = ['id', 'title', 'slug', 'lexer', 'code', 'line_count', 'stylized',
                  'key', 'public', 'blog_post', 'created', 'modified', 'publish_date',]
        validation = Validation()
        include_absolute_url = True
        detail_allowed_methods = ['get', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        ordering = ['created', 'modified',]
        # TODO max_limit does not work.
        max_limit = 200
        always_return_data = True
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['embed_url'] = bundle.obj.get_embed_url()
        bundle.data['tags_list'] = edit_string_for_tags(bundle.obj.tags.all())

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
        if type(bundle.data['tags']) == unicode:
            bundle.data['tags_list'] = bundle.data['tags']
        else:
            bundle.data['tags_list'] = ''
        bundle.data['tags'] = ''

        if 'blog_post' in bundle.data:
            bundle = self._clean_publish_date(bundle)

        return super(PrivateSniptResource, self).obj_update(bundle, request,
                     user=request.user, **kwargs)

    def _clean_publish_date(self, bundle):
        if bundle.data['blog_post'] and not bundle.data['publish_date']:
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
        # TODO max_limit does not work.
        max_limit = 200
        always_return_data = True
        cache = SimpleCache()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['user'] = request.user
        bundle.data['snipt'] = Snipt.objects.get(pk=bundle.data['snipt'])
        return super(PrivateFavoriteResource, self).obj_create(bundle, request,
                     user=request.user, **kwargs)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
