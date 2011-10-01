from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

from views import home

from snipts.api import SniptResource

snipt_resource = SniptResource()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^404/$', direct_to_template, {'template': '404.html'}),
    url(r'^500/$', direct_to_template, {'template': '500.html'}),

    url(r'^api/', include(snipt_resource.urls)),

    url(r'^$', home),
)
