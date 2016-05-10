import datetime
import os
import stripe

from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from snipts.models import Snipt


@login_required
@render_to('account.html')
def account(request):
    return {}


@login_required
@render_to('activate.html')
def activate(request):

    if request.method == 'POST':

        token = request.POST['token']
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY',
                                        settings.STRIPE_SECRET_KEY)

        try:
            customer = stripe.Customer.create(card=token,
                                              email=request.user.email)
            stripe.Charge.create(amount=900,
                                 currency='usd',
                                 customer=customer.id,
                                 description='Snipt.net')
        except stripe.CardError as e:
            error_message = e.json_body['error']['message']
            return HttpResponseRedirect('/account/activate/?declined=%s' % error_message or
                                        'Your card was declined.')

        profile = request.user.profile
        profile.pro_date = datetime.datetime.now()
        profile.stripe_id = customer.id
        profile.save()

        request.user.is_active = True
        request.user.save()

        send_mail('[Snipt] New signup: {}'.format(request.user.username),
                  """
                  User: https://snipt.net/{}
                  Email: {}
                  """.format(request.user.username, request.user.email),
                  'support@snipt.net',
                  ['nick@snipt.net'],
                  fail_silently=False)

        return HttpResponseRedirect('/login-redirect/')

    else:
        return {}


@login_required
@render_to('stats.html')
def stats(request):

    snipts = Snipt.objects.filter(user=request.user).order_by('-views')

    return {
        'snipts': snipts
    }
