from tastypie.resources import ModelResource
from snipts.models import Snipt


class SniptResource(ModelResource):
    class Meta:
        queryset = Snipt.objects.all()
        resource_name = 'snipt'
