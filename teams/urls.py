from django.conf.urls import *
from teams import views


urlpatterns = \
    patterns('',
             url(r'^for-teams/$', views.for_teams),
             url(r'^for-teams/complete/$', views.for_teams_complete),
             url(r'^(?P<username>[^/]+)/members/remove/(?P<member>[^/]+)/$',
                 views.remove_team_member,
                 name='remove-team-member'),
             url(r'^(?P<username>[^/]+)/members/add/(?P<member>[^/]+)/$',
                 views.add_team_member,
                 name='add-team-member'),
             url(r'^(?P<username>[^/]+)/members/$',
                 views.team_members,
                 name='team-members'),
             url(r'^(?P<username>[^/]+)/billing/$',
                 views.team_billing,
                 name='team-billing'))
