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
def stripe_account_details(request):

    if request.user.profile.stripe_id is None:
        return {}
    else:
        stripe.api_key = STRIPE_SECRET_KEY
        customer = stripe.Customer.retrieve(request.user.profile.stripe_id)
        return {
            'last4': customer.active_card.last4,
            'created': customer.created,
            'email': customer.email,
            'amount': customer.subscription.plan.amount,
            'interval': customer.subscription.plan.interval,
            'name': customer.subscription.plan.name,
            'status': customer.subscription.status,
            'nextBill': customer.subscription.current_period_end,
        }


@login_required
@render_to('stats.html')
def stats(request):

    snipts = Snipt.objects.filter(user=request.user).order_by('-views')

    return {
        'snipts': snipts
    }
