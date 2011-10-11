from django.conf.urls.defaults import *

from snipts import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
)
