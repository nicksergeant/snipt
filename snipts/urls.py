from django.conf.urls.defaults import *

from snipts import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^(?P<user>[^/]+/)?$', views.list_user, name='list-user'),
)
