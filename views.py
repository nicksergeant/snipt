from annoying.decorators import ajax_request
from snipts.utils import get_lexers_list


@ajax_request
def lexers(request):
    return {'objects': get_lexers_list()}
