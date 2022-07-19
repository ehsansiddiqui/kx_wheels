from django.contrib import admin
from django.utils.translation import get_language, ugettext_lazy as _
from kxwheels.apps.l10n.models import Country, AdminArea, City, PostalCode

def make_country_active(modeladmin, request, queryset):
    queryset.update(active=True)
    make_country_active.short_description = "Mark selected as active"

def make_country_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
    make_country_inactive.short_description = "Mark selected as inactive"

class AdminArea_Inline(admin.TabularInline):
    model = AdminArea
    extra = 1

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_3166_1','active',)
    search_fields = ('name', 'iso_3166_1')
    inlines = [AdminArea_Inline]
    actions = [make_country_active, make_country_inactive]

class PostalCodeAdmin(admin.ModelAdmin):
    list_display = ('postal_code', 'location', 'city')
    search_fields = ('postal_code','city__name')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_3166_2',)
    list_filter = ('iso_3166_2',)
    search_fields = ('name',)

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(PostalCode, PostalCodeAdmin)

