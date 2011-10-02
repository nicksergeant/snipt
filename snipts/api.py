from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from snipts.models import Comment, Snipt
from tastypie import fields
from taggit.models import Tag

class PublicUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username',]
        include_absolute_url = True

class PublicCommentSniptResource(ModelResource):
    class Meta:
        queryset = Snipt.objects.filter(public=True).order_by('-created')
        resource_name = 'snipt'
        fields = ['id',]
        include_absolute_url = True

class PublicTagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        fields = ['name',]
        include_absolute_url = True

class PublicCommentResource(ModelResource):
    user = fields.ForeignKey(PublicUserResource, 'user')
    snipt = fields.ForeignKey(PublicCommentSniptResource, 'snipt')

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        fields = ['user', 'snipt', 'comment', 'created', 'modified',]
        include_absolute_url = True

class PublicSniptResource(ModelResource):
    comments = fields.ToManyField(PublicCommentResource, 'comment_set',related_name='comment')

    class Meta:
        queryset = Snipt.objects.filter(public=True).order_by('-created')
        resource_name = 'snipt'
        fields = ['user', 'title', 'slug', 'tags', 'lexer', 'code', 'stylized',
                  'created', 'modified',]
        include_absolute_url = True

    def dehydrate(self, bundle):
        bundle.data['user'] = {
            'username': bundle.obj.user.username,
            'resource_uri': '/api/public/user/%d/' % bundle.obj.user.id,
            'absolute_url': bundle.obj.user.get_absolute_url(),
        }

        bundle.data['tags'] = []
        for tag in bundle.obj.tags.all():
            bundle.data['tags'].append({
                'name': tag.name,
                'resource_uri': '/api/public/tag/%d/' % tag.id,
            })

        return bundle
