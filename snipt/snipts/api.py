from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from snipts.models import Snipt
from tastypie.cache import SimpleCache
from django.db.models import Count
from tastypie import fields
from taggit.models import Tag


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
        queryset = queryset.annotate(count=Count('taggit_taggeditem_items__id'))
        queryset = queryset.order_by('-count')
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
        fields = ['title', 'description', 'slug', 'lexer', 'code', 'line_count',
                  'created', 'modified',]
        include_absolute_url = True
        allowed_methods = ['get']
        filtering = { 'user': 'exact', }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['embed_url'] = bundle.obj.get_embed_url()
        bundle.data['stylized'] = bundle.obj.get_stylized()
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
        authentication = BasicAuthentication()
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
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['absolute_url'] = '/%s/tag/%s/' % (bundle.request.user.username,
                                                       bundle.obj.slug)
        bundle.data['snipts'] = '/api/private/snipt/?tag=%d' % bundle.obj.id

        bundle.data['count'] = bundle.obj.taggit_taggeditem_items.filter(
                               snipt__user=bundle.request.user).count()
                              
        return bundle

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(snipt__user=request.user)

class PrivateSniptResource(ModelResource):
    user = fields.ForeignKey(PrivateUserResource, 'user', full=True)
    tags = fields.ToManyField(PrivateTagResource, 'tags', related_name='tag', full=True)

    class Meta:
        queryset = Snipt.objects.all().order_by('-created')
        resource_name = 'snipt'
        fields = ['title', 'description', 'slug', 'lexer', 'code', 'line_count',
                  'key', 'public', 'created', 'modified',]
        include_absolute_url = True
        allowed_methods = ['get',]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['embed_url'] = bundle.obj.get_embed_url()
        bundle.data['stylized'] = bundle.obj.get_stylized()
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        return super(PrivateSniptResource, self).obj_create(bundle, request,
                     user=request.user)

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
