import os
import stripe
import uuid

from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.models import User
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


@render_to('teams/team-billing.html')
def team_billing(request, username):
    team = get_object_or_404(Team, slug=username)
    if team.owner != request.user:
        raise Http404
    return {
        'team': team
    }


@render_to('teams/team-members.html')
def team_members(request, username):
    team = get_object_or_404(Team, slug=username)
    return {
        'team': team
    }


def add_team_member(request, username, member):
    team = get_object_or_404(Team, slug=username)
    user = get_object_or_404(User, username=member)

    if (team.owner != request.user):
        raise Http404

    team.members.add(user)
    team.save()

    return HttpResponseRedirect('/' + team.slug + '/members/')


@render_to('teams/for-teams-complete.html')
def for_teams_complete(request):
    if request.method == 'POST' and request.user.is_authenticated():

        token = request.POST['token']
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY',
                                        settings.STRIPE_SECRET_KEY)

        plan = request.POST['plan']

        try:
            customer = stripe.Customer.create(card=token,
                                              plan=plan,
                                              email=request.user.email)
        except stripe.CardError, e:
            error_message = e.json_body['error']['message']
            return HttpResponseRedirect('/for-teams/?declined=%s' %
                                        error_message or
                                        'Your card was declined.')

        team = Team(name=request.POST['team-name'],
                    email=request.POST['email'],
                    plan=plan,
                    owner=request.user)
        team.stripe_id = customer.id
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
