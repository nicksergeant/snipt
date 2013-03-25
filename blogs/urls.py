from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', views.blog, name='blog'),
)
