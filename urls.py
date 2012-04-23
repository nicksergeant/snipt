from django.views.generic.simple import direct_to_template
from registration.forms import RegistrationFormUniqueEmail
from haystack.views import SearchView, search_view_factory
from django.http import HttpResponseRedirect
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from django.conf.urls.defaults import *
from django.contrib import admin
from django.db.models import Q
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

sqs = SearchQuerySet().filter(Q(public=True))

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^404/$', direct_to_template, {'template': '404.html'}),
    url(r'^500/$', direct_to_template, {'template': '500.html'}),

    url(r'^api/$', direct_to_template, {'template': 'api.html'}),
    url(r'^api/contest/$', direct_to_template, {'template': 'api-contest.html'}),

    url(r'^api/', include(public_api.urls)),
    url(r'^api/', include(private_api.urls)),

    url(r'^search/$', search_view_factory(
        view_class=SearchView,
        searchqueryset=sqs,
        form_class=ModelSearchForm,
    ), name='haystack_search'),

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
