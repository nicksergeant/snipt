from django.conf.urls.defaults import *

from snipts import views


urlpatterns = patterns('',
    url(r'^$',                                             views.home,          name='home'),
    url(r'^public/$',                                      views.list_public,   name='list-public'),
    url(r'^blog/$',                                        views.blog,          name='blog'),
    url(r'^public/tag/(?P<tag_slug>[^/]+)/$',              views.list_public,   name='list-public-tag'),
    url(r'^embed/(?P<snipt_key>[^/]+)/$',                  views.embed,         name='embed'),
    url(r'^raw/(?P<snipt_key>[^/]+)/$',                    views.raw,           name='raw'),
    url(r'^(?P<username_or_custom_slug>[^/]+)/$',          views.list_user,     name='list-user'),
    url(r'^(?P<username_or_custom_slug>[^/]+)/tag/(?P<tag_slug>[^/]+)/$', views.list_user, name='list-user-tag'),
    url(r'^(?P<username>[^/]+)/(?P<snipt_slug>[^/]+)/$',   views.detail,        name='detail'),
)
