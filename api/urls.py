from django.conf.urls.defaults import *

from piston.emitters import Emitter
from piston.resource import Resource

from api.handlers import SniptHandler


Emitter.unregister('django')
Emitter.unregister('pickle')
Emitter.unregister('yaml')

snipt_handler = Resource(SniptHandler)

urlpatterns = patterns('',
   url(r'^snipt/(?P<snipt_id>\d+)/', snipt_handler),
)
