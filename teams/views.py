import os
import uuid

from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from teams.models import Team


@render_to('teams/for-teams.html')
def for_teams(request):
    if request.user.is_authenticated():
        profile = request.user.profile
        profile.teams_beta_seen = True
        profile.save()
    return {}


@login_required
@render_to('teams/for-teams-complete.html')
def for_teams_complete(request):
    if request.method == 'POST' and request.user.is_authenticated():

        team = Team(name=request.POST['team-name'],
                    email=request.POST['email'],
                    owner=request.user)
        team.save()

        user = User.objects.create_user(team.slug,
                                        team.email,
                                        str(uuid.uuid4()))

        team.user = user
        team.save()

        send_mail('[Snipt] New team signup: {}'.format(team.name),
                  """
                  Team: https://snipt.net/{}
                  Email: {}
                  """.format(team.slug, team.email),
                  os.environ.get('POSTMARK_INBOUND_ADDRESS', 'snipt@localhost'),
                  ['nick@snipt.net'],
                  fail_silently=False)

        return {
            'team': team
        }
    else:
        return HttpResponseBadRequest()


@login_required
@render_to('teams/team-members.html')
def team_members(request, username):
    team = get_object_or_404(Team, slug=username, disabled=False)
    if not team.user_is_member(request.user):
        raise Http404
    return {
        'team': team
    }


@login_required
def add_team_member(request, username, member):
    team = get_object_or_404(Team, slug=username, disabled=False)
    user = get_object_or_404(User, username=member)

    if (team.owner != request.user):
        raise Http404

    if ((team.members.all().count() + 1) > team.member_limit):
        return HttpResponseRedirect('/' + team.slug +
                                    '/members/?limit-reached')
    else:
        team.members.add(user)
        return HttpResponseRedirect('/' + team.slug + '/members/')


@login_required
def remove_team_member(request, username, member):
    team = get_object_or_404(Team, slug=username, disabled=False)
    user = get_object_or_404(User, username=member)

    if (team.owner != request.user):
        raise Http404

    team.members.remove(user)

    return HttpResponseRedirect('/' + team.slug + '/members/')
