from views import amazon_search, amazon_image, lexers, sitemap, tags
from django.conf.urls.defaults import include, patterns, url
from django.views.generic.simple import direct_to_template
from registration.forms import RegistrationFormUniqueEmail
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

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^404/$', direct_to_template, {'template': '404.html'}),
    url(r'^500/$', direct_to_template, {'template': '500.html'}),

    url(r'^robots.txt$', direct_to_template, {'template': 'robots.txt'}),
    url(r'^humans.txt$', direct_to_template, {'template': 'humans.txt'}),
    url(r'^sitemap.xml$', sitemap),
    url(r'^pro/$', direct_to_template, {'template': 'pro.html'}),
    url(r'^tags/$', tags),

    url(r'^api/public/lexer/$', lexers),
    url(r'^api/public/a/$', amazon_search),
    url(r'^api/public/a/img/$', amazon_image),

    url(r'^api/', include(public_api.urls)),
    url(r'^api/', include(private_api.urls)),

    url(r'^search/$', search),

    url(r'^register/$', lambda x: HttpResponseRedirect('/signup/')),
    url(r'^signup/$',
        'registration.views.register', {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': RegistrationFormUniqueEmail,
        },
        name='registration_register'),
    url(r'', include('registration.backends.default.urls')),

    url(r'^', include('snipts.urls')),
)
