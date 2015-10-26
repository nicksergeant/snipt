import os
import stripe
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

        send_mail('[Snipt] New team signup: {}'.format(team.name),
                  """
                  Team: https://snipt.net/{}
                  Email: {}
                  Plan: {}
                  """.format(team.slug, team.email, team.plan),
                  'support@snipt.net',
                  ['nick@snipt.net'],
                  fail_silently=False)

        return {
            'team': team
        }
    else:
        return HttpResponseBadRequest()


@login_required
@render_to('teams/team-billing.html')
def team_billing(request, username):
    team = get_object_or_404(Team, slug=username, disabled=False)
    if team.owner != request.user:
        raise Http404

    if team.stripe_id == 'COMP':
        return {
            'name': 'Promotional trial',
            'team': team
        }

    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY',
                                    settings.STRIPE_SECRET_KEY)
    customer = stripe.Customer.retrieve(team.stripe_id)

    data = {
        'last4': customer.active_card.last4,
        'created': customer.created,
        'email': customer.email,
        'team': team
    }

    if customer.subscription:
        data['amount'] = customer.subscription.plan.amount
        data['interval'] = customer.subscription.plan.interval
        data['name'] = customer.subscription.plan.name
        data['status'] = customer.subscription.status
        data['nextBill'] = customer.subscription.current_period_end
    else:
        data['status'] = 'inactive'

    return data
    return {
        'team': team
    }


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


@login_required
def cancel_team_subscription(request, username):

    if request.method != 'POST':
        raise Http404

    team = get_object_or_404(Team, slug=username, disabled=False)
    if team.owner != request.user:
        raise Http404

    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY',
                                    settings.STRIPE_SECRET_KEY)
    customer = stripe.Customer.retrieve(team.stripe_id)
    customer.delete()

    team.disabled = True
    team.stripe_id = None
    team.plan = None
    team.save()

    send_mail('[Snipt] Team cancelled plan: {}'.format(team.name),
              """
              Team: https://snipt.net/{}
              Email: {}
              """.format(team.slug, team.email),
              'support@snipt.net',
              ['nick@snipt.net'],
              fail_silently=False)

    return HttpResponseRedirect('/' + team.slug + '/?team-cancelled=true')
