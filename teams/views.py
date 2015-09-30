import uuid

from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from teams.models import Team


@render_to('teams/for-teams.html')
def for_teams(request):
    if request.user.is_authenticated():
        profile = request.user.profile
        profile.teams_beta_seen = True
        profile.save()
    return {}


@render_to('teams/team-members.html')
def team_members(request, username):
    team = get_object_or_404(Team, slug=username)
    return {
        'team': team
    }


@render_to('teams/for-teams-complete.html')
def for_teams_complete(request):
    if request.method == 'POST' and request.user.is_authenticated():

        team = Team(name=request.POST['name'],
                    email=request.POST['email'],
                    owner=request.user)
        team.save()

        user = User.objects.create_user(team.slug,
                                        team.email,
                                        str(uuid.uuid4()))

        team.user = user
        team.save()

        return {
            'team': team
        }
    else:
        return HttpResponseBadRequest()
