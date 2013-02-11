from django.conf.urls.defaults import *

from accounts import views

urlpatterns = patterns('',
    url(r'^stats/$', views.stats,   name='account-stats'),
    url(r'^',       views.account, name='account-detail'),
)
