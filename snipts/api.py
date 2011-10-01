from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from snipts.models import Comment, Snipt
from tastypie.cache import SimpleCache
from taggit.models import Tag
from tastypie import fields

class PublicUserResource(ModelResource):
    class Meta:
        queryset      = User.objects.all()
        resource_name = 'user'
        fields        = ['username',]
        cache         = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['url'] = 'https://snipt.net/%s/' % bundle.obj.username
        return bundle

class PublicCommentSniptResource(ModelResource):
    class Meta:
        queryset      = Snipt.objects.filter(public=True).order_by('-created')
        resource_name = 'snipt'
        fields        = ['id',]
        cache         = SimpleCache()

class PublicTagResource(ModelResource):
    class Meta:
        queryset      = Tag.objects.all()
        resource_name = 'tag'
        fields        = ['name', 'slug',]
        cache         = SimpleCache()

class PublicCommentResource(ModelResource):
    user  = fields.ForeignKey(PublicUserResource, 'user')
    snipt = fields.ForeignKey(PublicCommentSniptResource, 'snipt')

    class Meta:
        queryset      = Comment.objects.all()
        resource_name = 'comment'
        fields        = ['user', 'snipt', 'comment', 'created', 'modified',]
        cache         = SimpleCache()

class PublicSniptResource(ModelResource):
    user              = fields.ForeignKey(PublicUserResource, 'user')
    comments          = fields.ToManyField(PublicCommentResource, 'comment_set',
                                  related_name='comment')
    tags              = fields.ToManyField(PublicTagResource, 'tags', related_name='tag')

    class Meta:
        queryset      = Snipt.objects.filter(public=True).order_by('-created')
        resource_name = 'snipt'
        fields        = ['user', 'title', 'slug', 'tags', 'lexer', 'code', 'stylized',
                         'created', 'modified',]
        cache         = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data['url']           = bundle.obj.get_absolute_url()
        bundle.data['user_username'] = bundle.obj.user.username
        bundle.data['user_url']      = 'https://snipt.net/%s/' % bundle.obj.user.username
        return bundle
