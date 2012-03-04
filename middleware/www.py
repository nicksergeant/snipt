import re

from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect


class WWWMiddleware(object):

    def process_request(self, request):
        url = request.build_absolute_uri(request.get_full_path())
        if 'www.' in url:
            non_www_url = url.replace('www.', '')
            return HttpResponseRedirect(non_www_url)
