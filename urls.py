from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import admin
from snipts.api import (PublicSniptResource,
                        PublicUserResource, PrivateSniptResource,
                        PrivateFavoriteResource, PrivateUserProfileResource,
                        PrivateUserResource, PublicTagResource)
from snipts.views import search
from tastypie.api import Api
from utils.views import SniptRegistrationView
from jobs.views import jobs, jobs_json
from views import (homepage, lexers, login_redirect, pro, sitemap, tags,
                   pro_complete, user_api_key)

import admin as custom_admin
import os


admin.autodiscover()

public_api = Api(api_name='public')
public_api.register(PublicSniptResource())
public_api.register(PublicTagResource())
public_api.register(PublicUserResource())

private_api = Api(api_name='private')
private_api.register(PrivateSniptResource())
private_api.register(PrivateUserResource())
private_api.register(PrivateFavoriteResource())
private_api.register(PrivateUserProfileResource())

urlpatterns = patterns('',

    url(r'^$', homepage),
    url(r'^login-redirect/$', login_redirect),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),

    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^humans.txt$', TemplateView.as_view(template_name='humans.txt')),
    url(r'^sitemap.xml$', sitemap),
    url(r'^tags/$', tags),

    url(r'^pro/$', pro),
    url(r'^pro/complete/$', pro_complete),

    url(r'^account/', include('accounts.urls')),

    url(r'^api/public/lexer/$', lexers),

    url(r'^api/private/key/$', user_api_key),
    url(r'^api/', include(public_api.urls)),
    url(r'^api/', include(private_api.urls)),

    url(r'^search/$', search),

    url(r'^register/$', lambda x: HttpResponseRedirect('/signup/')),
    url(r'^signup/$', SniptRegistrationView.as_view(),
        name='registration_register'),
    url(r'', include('registration.backends.default.urls')),

    url(r'^', include('snipts.urls')),
)
