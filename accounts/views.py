from django.contrib.auth.decorators import login_required
from annoying.decorators import ajax_request, render_to
from snipts.models import Snipt

import stripe

from settings_local import STRIPE_SECRET_KEY


@login_required
@render_to('account.html')
def account(request):
    return {}


@login_required
@ajax_request
def cancel_subscription(request):

    if request.user.profile.stripe_id is None:
        return {}
    else:
        stripe.api_key = STRIPE_SECRET_KEY
        customer = stripe.Customer.retrieve(request.user.profile.stripe_id)
        customer.delete()

        profile = request.user.profile
        profile.is_pro = False
        profile.stripe_id = None
        profile.save()

        return { 'deleted': True }

@login_required
@ajax_request
def stripe_account_details(request):

    if request.user.profile.stripe_id is None:
        return {}
    else:
        stripe.api_key = STRIPE_SECRET_KEY
        customer = stripe.Customer.retrieve(request.user.profile.stripe_id)

        data = {
            'last4': customer.active_card.last4,
            'created': customer.created,
            'email': customer.email,
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


@login_required
@render_to('stats.html')
def stats(request):

    snipts = Snipt.objects.filter(user=request.user).order_by('-views')

    return {
        'snipts': snipts
    }
