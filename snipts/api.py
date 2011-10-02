from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from snipts.models import Comment, Snipt
from django.db.models import Count
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
        tags = Tag.objects.filter(snipt__public=True)
        annotated = tags.annotate(count=Count('taggit_taggeditem_items__id'))
        queryset = annotated.order_by('-count')
        resource_name = 'tag'
        fields = ['name',]

    def dehydrate(self, bundle):
        bundle.data['absolute_url'] = '/public/tag/%s/' % bundle.obj.slug
        bundle.data['snipts'] = '/api/public/snipt/?tag=%d' % bundle.obj.id
        bundle.data['count'] = bundle.obj.taggit_taggeditem_items.filter(snipt__public=True).count()
        return bundle

class PublicCommentResource(ModelResource):
    user = fields.ForeignKey(PublicUserResource, 'user')
    snipt = fields.ForeignKey(PublicCommentSniptResource, 'snipt')

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        fields = ['user', 'snipt', 'comment', 'created', 'modified',]
        include_absolute_url = True

class PublicSniptResource(ModelResource):
    comments = fields.ToManyField(PublicCommentResource, 'comment_set',
                                  related_name='comment')

    class Meta:
        queryset = Snipt.objects.filter(public=True).order_by('-created')
        resource_name = 'snipt'
        fields = ['user', 'title', 'slug', 'tags', 'lexer', 'code', 'created',
                  'modified',]
        include_absolute_url = True

    def dehydrate(self, bundle):
        bundle.data['user'] = {
            'username': bundle.obj.user.username,
            'resource_uri': '/api/public/user/%d/' % bundle.obj.user.id,
            'absolute_url': bundle.obj.user.get_absolute_url(),
        }

        bundle.data['embed_url'] = bundle.obj.embed_url
        bundle.data['stylized'] = bundle.obj.get_stylized()

        bundle.data['tags'] = []
        for tag in bundle.obj.tags.all():
            bundle.data['tags'].append({
                'name': tag.name,
                'count': tag.taggit_taggeditem_items.filter(snipt__public=True).count(),
                'absolute_url': '/public/tag/%s/' % tag.slug,
                'resource_uri': '/api/public/tag/%d/' % tag.id,
                'snipts': '/api/public/snipt/?tag=%d' % tag.id,
            })

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
