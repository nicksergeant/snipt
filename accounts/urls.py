from accounts import views
from django.conf.urls import url


urlpatterns = [
     url(r'^stats/$', views.stats, name='account-stats'),
     url(r'^', views.account, name='account-detail')
]
