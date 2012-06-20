from django.shortcuts import render_to_response
from annoying.decorators import ajax_request
from django.template import RequestContext
from snipts.utils import get_lexers_list


def sitemap(request):
    return render_to_response('sitemap.xml',
                              {},
                              context_instance=RequestContext(request),
                              mimetype='application/xml')

@ajax_request
def lexers(request):
    lexers = get_lexers_list()
    objects = []

    for l in lexers:

        try:
            filters = l[2]
        except IndexError:
            filters = []

        try:
            mimetypes = l[3]
        except IndexError:
            mimetypes = []

        objects.append({
            'name': l[0],
            'lexers': l[1],
            'filters': filters,
            'mimetypes': mimetypes
        })

    return {'objects': objects}
