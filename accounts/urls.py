from accounts import views
from django.conf.urls import *

urlpatterns = \
    patterns('',
             url(r'^stats/$', views.stats, name='account-stats'),
             url(r'^', views.account, name='account-detail'))
