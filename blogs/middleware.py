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

                    blog_user = ''.join(host_s[:-2])

                    if '-' in blog_user:
                        request.blog_user = get_object_or_None(User, username__iexact=blog_user)

                        if request.blog_user is None:
                            request.blog_user = get_object_or_404(User, username__iexact=blog_user.replace('-', '_'))
                    else:
                        request.blog_user = get_object_or_404(User, username__iexact=blog_user)

            if request.blog_user is None:
                pro_users = User.objects.filter(userprofile__is_pro=True, username='nick')

                for pro_user in pro_users:
                    if host == pro_user.profile.blog_domain:
                        request.blog_user = pro_user
