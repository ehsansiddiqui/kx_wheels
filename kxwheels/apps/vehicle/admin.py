from django.contrib import admin
from kxwheels.apps.vehicle.models import *

class TreadWidthAdmin(admin.ModelAdmin):
    list_display = ('value', 'ordering')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('value', 'ordering')

class DiameterAdmin(admin.ModelAdmin):
    list_display = ('value', 'ordering')

class BoltPatternAdmin(admin.ModelAdmin):
    list_display = ('value', 'sort_order')

class WheelWidthAdmin(admin.ModelAdmin):
    list_display = ('value', 'sort_order')

class FinishAdmin(admin.ModelAdmin):
    list_display = ('value', 'sort_order')
    
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', )
    prepopulated_fields = {"slug": ("name",)}

# Wheel #
class FrontWheelSizeInline(admin.TabularInline):
    model = FrontWheelSize

class RearWheelSizeInline(admin.TabularInline):
    model = RearWheelSize
# End Wheel #

# Tire #
class OETireSizeInline(admin.TabularInline):
    model = OETireSize
    extra = 3
    
class OEStaggeredTireSizeInline(admin.TabularInline):
    model = OEStaggeredTireSize
    extra = 3

class PlusTireSizeInline(admin.TabularInline):
    model = PlusTireSize
    extra = 3
    
class PlusStaggeredTireSizeInline(admin.TabularInline):
    model = PlusStaggeredTireSize
    extra = 3
# End Tire #

class TPMSAdmin(admin.ModelAdmin):
    raw_id_fields = ('vehicle',)
    search_fields = ('vehicle__name',)

class ModelAdmin(admin.ModelAdmin):
    inlines = [FrontWheelSizeInline, RearWheelSizeInline, OETireSizeInline, 
        OEStaggeredTireSizeInline, PlusTireSizeInline, PlusStaggeredTireSizeInline]
    list_display = ('year', 'manufacturer', 'name',)
    list_display_links = ('year', 'manufacturer', 'name',)
    list_filter = ('manufacturer', )
    search_fields = ['name']
    prepopulated_fields = {"slug": ("year", "name",)}

admin.site.register(TreadWidth, TreadWidthAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Diameter, DiameterAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(BoltPattern, BoltPatternAdmin)
admin.site.register(WheelWidth, WheelWidthAdmin)
admin.site.register(Finish, FinishAdmin)
admin.site.register(TPMS, TPMSAdmin)
