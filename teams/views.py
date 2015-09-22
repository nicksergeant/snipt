from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from teams.models import Team


@render_to('teams/for-teams.html')
def for_teams(request):
    if request.user.is_authenticated():
        profile = request.user.profile
        profile.teams_beta_seen = True
        profile.save()
    return {}


@render_to('teams/for-teams-complete.html')
def for_teams_complete(request):
    if request.method == 'POST' and request.user.is_authenticated():

        team = Team(name=request.POST['name'],
                    email='nick@snipt.net',
                    owner=request.user)
        team.save()

        user = User.objects.create_user(team.slug, team.email, 'password')

        team.user = user
        team.save()

        return {

        }
    else:
        return HttpResponseBadRequest()
