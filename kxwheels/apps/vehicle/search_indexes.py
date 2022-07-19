from haystack import indexes
from kxwheels.apps.vehicle.models import Model

class ModelIndex(indexes.SearchIndex, indexes.Indexable):
    model_id = indexes.IntegerField(model_attr='id')
    text = indexes.CharField(document=True, model_attr='name', use_template=True)
    manufacturer = indexes.CharField(model_attr='manufacturer')
    manufacturer_slug = indexes.CharField(model_attr='manufacturer__slug', indexed=False)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug', indexed=False)
    year = indexes.IntegerField(model_attr='year')

    def get_model(self):
        return Model

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related('manufacturer__slug').all()
