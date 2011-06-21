from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc

from snipts.models import Snipt


class AnonSniptHandler(AnonymousBaseHandler):
    model = Snipt
    fields = ('title',)

    def read(self, request, snipt_id):
        return super(self.read)

class SniptHandler(BaseHandler):
    allowed_methods = ('GET',)
    anonymous = AnonSniptHandler
    exclude = ('id',)
    model = Snipt

    def read(self, request, snipt_id):
        """
        Returns an individual public or private snipt.
        """

        if snipt_id:
            try:
                return Snipt.objects.get(pk=snipt_id, public=True)
            except Snipt.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return rc.BAD_REQUEST
