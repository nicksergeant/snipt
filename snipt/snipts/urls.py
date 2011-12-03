from django.conf.urls.defaults import *

from snipts import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^public/$', views.list_public, name='list-public'),
    url(r'^public/tag/(?P<tag>[^/]+)/$', views.list_public, name='list-public-tag'),
    url(r'^(?P<user>[^/]+)/$', views.list_user, name='list-user'),
    url(r'^(?P<user>[^/]+)/tag/(?P<tag>[^/]+)/$', views.list_user, name='list-user-tag'),
)
