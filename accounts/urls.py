from django.conf.urls import *

from accounts import views

urlpatterns = \
    patterns('',
             url(r'^stats/$', views.stats, name='account-stats'),
             url(r'^cancel-subscription/$', views.cancel_subscription,
                 name='cancel-subscription'),
             url(r'^stripe-account-details/$', views.stripe_account_details,
                 name='stripe-account-details'),
             url(r'^', views.account, name='account-detail'))
