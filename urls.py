from views import (homepage, lexers, pro_signup, sitemap, tags, pro_signup_complete)
from django.conf.urls import include, patterns, url
from utils.views import SniptRegistrationView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import admin
from snipts.views import search
from tastypie.api import Api
from snipts.api import *

import admin as custom_admin


admin.autodiscover()

public_api = Api(api_name='public')
public_api.register(PublicSniptResource())
public_api.register(PublicTagResource())
public_api.register(PublicUserResource())

private_api = Api(api_name='private')
private_api.register(PrivateSniptResource())
private_api.register(PrivateTagResource())
private_api.register(PrivateUserResource())
private_api.register(PrivateFavoriteResource())
private_api.register(PrivateUserProfileResource())

urlpatterns = patterns('',

    url(r'^homepage/$', homepage),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),

    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^humans.txt$', TemplateView.as_view(template_name='humans.txt')),
    url(r'^sitemap.xml$', sitemap),
    url(r'^tags/$', tags),

    url(r'^pro/$', TemplateView.as_view(template_name='pro.html')),
    url(r'^pro/signup/$', pro_signup),
    url(r'^pro/signup/complete/$', pro_signup_complete),

    url(r'^account/', include('accounts.urls')),

    url(r'^api/public/lexer/$', lexers),

    url(r'^api/', include(public_api.urls)),
    url(r'^api/', include(private_api.urls)),

    url(r'^search/$', search),

    url(r'^register/$', lambda x: HttpResponseRedirect('/signup/')),
    url(r'^signup/$',
        SniptRegistrationView.as_view(),
        name='registration_register'),
    url(r'', include('registration.backends.default.urls')),

    url(r'^', include('snipts.urls')),
)
