from django.contrib import admin
from kxwheels.apps.kx.models.wheel import WheelSliderImages
from kxwheels.apps.kx.models.accessories import *
from kxwheels.apps.kx.models import (Task,
                       TireManufacturer,
                       FeaturedBrand,
                       TireCategory,
                       Tire,
                       TirePicture,
                       TireReview,
                       TireCoupon,
                       TireCustomerMedia,
                       TireSize,
                       WheelManufacturer,
                       Wheel,
                       WheelPicture,
                       WheelReview,
                       WheelCoupon,
                       WheelCustomerMedia,
                       WheelSize,)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering', 'is_active',)
    prepopulated_fields = {"slug": ("name",)}

class FeaturedAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering', 'is_active',)
    prepopulated_fields = {"slug": ("name",)}

# Tire


class TireCoupon_Inline(admin.StackedInline):
    model = TireCoupon
    extra = 1


class TireCustomerMedia_Inline(admin.StackedInline):
    model = TireCustomerMedia
    extra = 1


class TireSize_Inline(admin.TabularInline):
    #list_display = ('prefix', 'treadwidth', 'profile', 'diameter',)
    model = TireSize
    extra = 1
    exclude = ('part_no', 'name', 'quantity', 'cost', 'meta_title', 'meta_keywords',
               'meta_description', 'short_desc', 'long_desc', 'slug', 'is_active', 'options',
               'special_price', 'spvf', 'spvt', 'site', "width", "width_unit", "height",
               "height_unit", "length", "length_unit",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(TireSize_Inline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ["sku", "price", "weight", "weight_unit",
                             "utgq_rating", "load_rating", "sidewall_style", "additional_size",
                             "treadwidth", "profile", "diameter"]:
            field.widget.attrs['style'] = "width:60px"
        if db_field.name in ["prefix", "ply"]:
            field.widget.attrs['style'] = "width:50px"
        if db_field.name == 'weight_unit':
            field.initial = 'lbs'

        return field


class TirePicture_Inline(admin.TabularInline):
    model = TirePicture
    extra = 3


class TireAdmin(admin.ModelAdmin):
    inlines = [
        TirePicture_Inline,
        TireCoupon_Inline,
        TireCustomerMedia_Inline,
        TireSize_Inline,
        ]
    #list_display = ('name', 'manufacturer', )
    list_filter = ('manufacturer', )
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
    #raw_id_fields = ("manufacturer",)

class TireCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering',)
    prepopulated_fields = {"slug": ("name",)}


class TireReviewAdmin(admin.ModelAdmin):
    model = TireReview
    raw_id_fields = ('reviewee',)

# Wheel


class WheelCouponInline(admin.StackedInline):
    model = WheelCoupon
    extra = 1


class WheelCustomerMediaInline(admin.StackedInline):
    model = WheelCustomerMedia
    extra = 1


class WheelSizeInline(admin.TabularInline):
    model = WheelSize
    extra = 0
    exclude = ('name', 'quantity', 'cost', 'meta_title', 'meta_keywords',
               'meta_description', 'short_desc', 'long_desc', 'slug', 'is_active', 'options',
               'special_price', 'spvf', 'spvt', 'site', "width", "width_unit", "height",
               "height_unit", "length", "length_unit",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(WheelSizeInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in [ "sku", "price", "weight", "weight_unit", "part_no",
                              "wheelwidth", "profile", "diameter", "finish", "boltpattern_1",
                              "boltpattern_2", "centerbore"]:
            field.widget.attrs['style'] = "width:60px"
        if db_field.name in [ "prefix", "ply"]:
            field.widget.attrs['style'] = "width:50px"
        if db_field.name == 'weight_unit':
            field.initial = 'lbs'

        return field


class WheelPictureInline(admin.TabularInline):
    model = WheelPicture
    extra = 3


class WheelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        WheelPictureInline,
        WheelCouponInline,
        WheelCustomerMediaInline,
        WheelSizeInline,
    ]
    search_fields = ['name',]


class WheelReviewAdmin(admin.ModelAdmin):
    model = WheelReview
    raw_id_fields = ('reviewee',)


class WheelSizeAdmin(admin.ModelAdmin):
    search_fields = ['wheel__name','sku',]


class TireSizeAdmin(admin.ModelAdmin):
    search_fields = ['tire__name','sku',]


class WheelPictureAdmin(admin.ModelAdmin):
    list_display = ('wheel',)
    search_fields = ['wheel__name',]


class WheelSliderImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'image_link',)


class AccessoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


class AccessoriesPictureInline(admin.TabularInline):
    model = AccessoriesPicture
    extra = 3


class AccessoriesCouponInline(admin.StackedInline):
    model = AccessoriesCoupon
    extra = 1


class AccessoriesDetailInline(admin.TabularInline):
    model = AccessoriesDetail
    extra = 0
    exclude = ('name', 'quantity', 'cost', 'meta_title', 'meta_keywords',
               'meta_description', 'short_desc', 'long_desc', 'slug', 'is_active', 'options',
               'special_price', 'spvf', 'spvt', 'site', "width", "width_unit", "height",
               "height_unit", "length", "length_unit")

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AccessoriesDetailInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ["sku", "price", "weight", "weight_unit", "part_no",
                              "accessoriewidth", "profile", "finish"]:
            field.widget.attrs['style'] = "width:80px"
        if db_field.name in [ "prefix", "ply"]:
            field.widget.attrs['style'] = "width:50px"
        if db_field.name == 'weight_unit':
            field.initial = 'lbs'

        return field


class AccessoriesCustomerMediaInline(admin.StackedInline):
    model = AccessoriesCustomerMedia
    extra = 1


class AccessoriesListAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        AccessoriesPictureInline,
        AccessoriesCouponInline,
        AccessoriesCustomerMediaInline,
        AccessoriesDetailInline,
    ]
    search_fields = ['name', ]


admin.site.register(Task)
admin.site.register(Accessories, AccessoriesAdmin)
admin.site.register(AccessoriesList, AccessoriesListAdmin)
admin.site.register(TireCategory, TireCategoryAdmin)
admin.site.register(TireManufacturer, ManufacturerAdmin)
admin.site.register(Tire, TireAdmin)
admin.site.register(TireSize, TireSizeAdmin)
admin.site.register(TireReview, TireReviewAdmin)

admin.site.register(WheelManufacturer, ManufacturerAdmin)
admin.site.register(FeaturedBrand, FeaturedAdmin)
admin.site.register(Wheel, WheelAdmin)
admin.site.register(WheelSize, WheelSizeAdmin)
admin.site.register(WheelReview, WheelReviewAdmin)
admin.site.register(WheelPicture, WheelPictureAdmin)
admin.site.register(WheelSliderImages, WheelSliderImagesAdmin)
