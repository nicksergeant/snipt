from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', views.blog, name='blog'),
    url(r'^login/$', lambda x: HttpResponseRedirect('https://snipt.net/login/')),
)
