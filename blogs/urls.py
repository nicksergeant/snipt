from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', views.blog_homepage, name='blog-homepage'),
    url(r'^blog/$', views.blog, name='blog'),
)
