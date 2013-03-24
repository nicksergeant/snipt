import datetime
from haystack import indexes
from snipts.models import Snipt


class SniptIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='created')
    public = indexes.BooleanField(model_attr='public')
    typ = indexes.CharField(model_attr='lexer')

    def get_model(self):
        return Snipt

    def index_queryset(self, **kwargs):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())
