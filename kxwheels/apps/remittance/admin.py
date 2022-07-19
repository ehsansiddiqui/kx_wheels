from django.contrib import admin
from .models import *

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PurchaseItemInline, 
            self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in [ "sku", "qty", "unit_price", 
            "discount", "ext_price", "tax"]:
            field.widget.attrs['style'] = "width:80px"
        if db_field.name == "desc":
            field.widget.attrs['style'] = "width:50px; height:40px"
        return field

class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseItemInline]
    search_fields = ('order',)
    
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Transaction)
admin.site.register(Seller)
admin.site.register(Buyer)
