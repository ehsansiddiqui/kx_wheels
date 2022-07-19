from haystack import indexes
from kxwheels.apps.kx.models import TireSize, WheelSize


class TireSizeIndex(indexes.SearchIndex, indexes.Indexable):
    tiresize_id = indexes.IntegerField(model_attr='id')
    text = indexes.CharField(document=True, model_attr='tire', use_template=True)
    tire = indexes.CharField(model_attr='tire')
    tire_slug = indexes.CharField(model_attr='tire__slug', indexed=False)
    manufacturer = indexes.CharField(model_attr='tire__manufacturer')
    manufacturer_slug = indexes.CharField(model_attr='tire__manufacturer__slug', indexed=False)
    manufacturer_logo = indexes.CharField(model_attr='tire__manufacturer__picture', indexed=False)
    category = indexes.CharField(model_attr='tire__category')
    #part_no = CharField(model_attr='part_no', indexed=False)
    sku = indexes.CharField(model_attr='sku', indexed=False)

    prefix = indexes.CharField(model_attr='prefix')
    treadwidth = indexes.CharField(model_attr='treadwidth')
    profile = indexes.CharField(model_attr='profile')
    diameter = indexes.DecimalField(model_attr='diameter')
    ply = indexes.CharField(model_attr='ply')
    speed_rating = indexes.CharField(model_attr='speed_rating')
    load_rating = indexes.CharField(model_attr='load_rating')

    additional_size = indexes.CharField(model_attr='additional_size', indexed=False)
    sidewall_style = indexes.CharField(model_attr='sidewall_style', indexed=False)
    utgq_rating = indexes.CharField(model_attr='utgq_rating', indexed=False)

    availability = indexes.CharField(model_attr='availability', indexed=False)
    quantity = indexes.CharField(model_attr='quantity', indexed=False)
    price = indexes.DecimalField(model_attr='price',)

    thumbnail_lg = indexes.CharField(indexed=False)
    thumbnail_med = indexes.CharField(indexed=False)
    thumbnail_sm = indexes.CharField(indexed=False)

    def get_model(self):
        return TireSize

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.select_related('tire__slug',
                                                       'tire__category',
                                                       'tire__manufacturer__slug',
                                                       'tire__manufacturer__picture',).all()

    def prepare_diameter(self, obj):
        return obj.get_diameter()

    def prepare_thumbnail_lg(self, obj):
        try:
            thumbnail = obj.tire.pictures.all()[0].thumbnails.filter(size="lg")[0].path
        except:
            thumbnail = None
        return thumbnail

    def prepare_thumbnail_med(self, obj):
        try:
            thumbnail = obj.tire.pictures.all()[0].thumbnails.filter(size="med")[0].path
        except:
            thumbnail = None
        return thumbnail

    def prepare_thumbnail_sm(self, obj):
        try:
            thumbnail = obj.tire.pictures.all()[0].thumbnails.filter(size="sm")[0].path
        except:
            thumbnail = None
        return thumbnail


class WheelSizeIndex(indexes.SearchIndex, indexes.Indexable):
    wheelsize_id = indexes.IntegerField(model_attr='id')
    text = indexes.CharField(document=True, model_attr='wheel', use_template=True)
    manufacturer = indexes.CharField(model_attr='wheel__manufacturer')
    manufacturer_slug = indexes.CharField(model_attr='wheel__manufacturer__slug', indexed=False)
    wheel = indexes.CharField(model_attr='wheel')
    wheel_slug = indexes.CharField(model_attr='wheel__slug', indexed=False)
    sku = indexes.CharField(model_attr='sku', indexed=False)
    diameter = indexes.DecimalField(model_attr='diameter')
    wheelwidth = indexes.FloatField(model_attr='wheelwidth')
    offset = indexes.IntegerField(model_attr='offset')
    finish = indexes.CharField(model_attr='finish')
    centerbore = indexes.CharField(model_attr='centerbore')
    boltpattern_1 = indexes.CharField(model_attr='boltpattern_1')
    boltpattern_2 = indexes.CharField(model_attr='boltpattern_2')
    quantity = indexes.CharField(model_attr='quantity')
    price = indexes.DecimalField(model_attr='price')

    thumbnail_lg = indexes.CharField(indexed=False)
    thumbnail_med = indexes.CharField(indexed=False)
    thumbnail_sm = indexes.CharField(indexed=False)

    def get_model(self):
        return WheelSize

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.select_related('wheel__slug',
                                                       'wheel__manufacturer__slug').all()

    def prepare_diameter(self, obj):
        return obj.get_diameter()

    def prepare_wheelwidth(self, obj):
        return obj.get_wheelwidth()

    def prepare_thumbnail_lg(self, obj):
        try:
            thumbnail = obj.wheel.pictures.all()[0].thumbnails.filter(size="lg")[0].path
        except:
            thumbnail = None
        return thumbnail

    def prepare_thumbnail_med(self, obj):
        try:
            thumbnail = obj.wheel.pictures.all()[0].thumbnails.filter(size="med")[0].path
        except:
            thumbnail = None
        return thumbnail

    def prepare_thumbnail_sm(self, obj):
        try:
            thumbnail = obj.wheel.pictures.all()[0].thumbnails.filter(size="sm")[0].path
        except:
            thumbnail = None
        return thumbnail

#class WheelIndex(SearchIndex):
#    text = CharField(document=True, model_attr='name', use_template=True)
#    manufacturer = CharField(model_attr='manufacturer')
#    manufacturer_slug = CharField(model_attr='manufacturer__slug', indexed=False)
#    wheel_slug = CharField(model_attr='slug', indexed=False)
#    diameter = DecimalField(model_attr='sizes__diameter')
#    wheelwidth = FloatField(model_attr='sizes__wheelwidth')
#    offset = IntegerField(model_attr='sizes__offset')
#    finish = CharField(model_attr='sizes__finish')
#    centerbore = CharField(model_attr='sizes__centerbore')
#    boltpattern_1 = CharField(model_attr='sizes__boltpattern_1')
#    boltpattern_2 = CharField(model_attr='sizes__boltpattern_2')
#    quantity = CharField(model_attr='sizes__quantity')
#    price = DecimalField(model_attr='sizes__price')

