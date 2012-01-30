from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from tastypie.api import Api
from snipts.api import *

import admin as custom_admin

admin.autodiscover()

public_api = Api(api_name='public')
public_api.register(PublicSniptResource())
public_api.register(PublicTagResource())
public_api.register(PublicUserResource())

private_api = Api(api_name='private')
private_api.register(PrivateSniptResource())
private_api.register(PrivateTagResource())
private_api.register(PrivateUserResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^404/$', direct_to_template, {'template': '404.html'}),
    url(r'^500/$', direct_to_template, {'template': '500.html'}),

    url(r'^api/', include(public_api.urls)),
    url(r'^api/', include(private_api.urls)),

    url(r'^', include('snipts.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
