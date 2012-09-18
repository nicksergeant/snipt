from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from annoying.functions import get_object_or_None


class BlogMiddleware:
    def process_request(self, request):
        request.blog_user = None

        host = request.META.get('HTTP_HOST', '')
        host_s = host.replace('www.', '').split('.')

        if host != 'snipt.net' and host != 'snipt.localhost':
            if len(host_s) > 2:
                if host_s[1] == 'snipt':
                    # nick.snipt.net or nick.snipt.localhost

                    blog_user = ''.join(host_s[:-2])

                    if '-' in blog_user:
                        request.blog_user = get_object_or_None(User, username__iexact=blog_user)

                        if request.blog_user is None:
                            request.blog_user = get_object_or_404(User, username__iexact=blog_user.replace('-', '_'))
                    else:
                        request.blog_user = get_object_or_404(User, username__iexact=blog_user)

        # TODO: build this into account settings.
        if host == 'rochacbruno.com.br':
            request.blog_user = User.objects.get(id=2156)

        if host == 'snipt.joshhudnall.com':
            request.blog_user = User.objects.get(id=10325)

        if host == 'nicksergeant.com':
            request.blog_user = User.objects.get(id=3)

        if host == 'ashleysergeant.com':
            request.blog_user = User.objects.get(id=18)
