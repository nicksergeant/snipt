from taggit.utils import edit_string_for_tags, parse_tags
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.validation import Validation
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from tastypie.models import create_api_key
from tastypie.cache import SimpleCache
from tastypie.fields import ListField
from snipts.forms import SniptForm
from snipts.models import Snipt
from taggit.models import Tag
from django.db import models
from tastypie import fields

models.signals.post_save.connect(create_api_key, sender=User)


class PublicUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username',]
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
        fields = ['name',]
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
        fields = ['title', 'slug', 'lexer', 'code', 'line_count',
                  'stylized', 'created', 'modified',]
        include_absolute_url = True
        allowed_methods = ['get']
        filtering = { 'user': 'exact', }
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

        return orm_filters


class PrivateUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'email',]
        include_absolute_url = True
        allowed_methods = ['get']
        list_allowed_methods = []
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        cache = SimpleCache()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(username=request.user.username)

class PrivateTagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        fields = ['name',]
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
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
        fields = ['title', 'slug', 'lexer', 'code', 'line_count',
                  'stylized', 'key', 'public', 'created', 'modified',]
        validation = Validation()
        include_absolute_url = True
        detail_allowed_methods = ['get', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['embed_url'] = bundle.obj.get_embed_url()
        bundle.data['tags_list'] = edit_string_for_tags(bundle.obj.tags.all())
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['tags_list'] = bundle.data.get('tags')
        bundle.data['tags'] = ''
        return super(PrivateSniptResource, self).obj_create(bundle, request,
                     user=request.user)

    def obj_update(self, bundle, request=None, **kwargs):
        bundle.data['user'] = request.user
        if type(bundle.data['tags']) == unicode:
            bundle.data['tags_list'] = bundle.data['tags']
        else:
            bundle.data['tags_list'] = ''
        bundle.data['tags'] = ''
        return super(PrivateSniptResource, self).obj_update(bundle, request, **kwargs)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(PrivateSniptResource, self).build_filters(filters)

        if 'tag' in filters:
            tag = Tag.objects.get(pk=filters['tag'])
            tagged_items = tag.taggit_taggeditem_items.all()
            orm_filters['pk__in'] = [i.object_id for i in tagged_items]

        return orm_filters

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def save_m2m(self, bundle):
        tags = bundle.data.get('tags_list', [])
        if tags != '':
            bundle.obj.tags.set(*parse_tags(tags))
