from django.conf import settings
from django.contrib import admin

from kxwheels.apps.shop.forms import AdminTaxRateForm, AdminOrderForm
from kxwheels.apps.shop.models import (Setting, Cart, CartItem, CartShipping, Order,
                                       OrderNote, OrderItem, TaxClass, TaxRate, Discount, Option, ProductOption,
                                       Payment)


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 5

class OptionAdmin(admin.ModelAdmin):
    inlines = [ProductOptionInline, ]
    
    def change_view(self, request, object_id, extra_context=None):
        result = super(OptionAdmin, self).change_view(request, object_id, extra_context)
        next_page = request.GET.get('next', None)
        if next_page is not None:
            result['Location'] = next_page
        return result
        
class ProductAdmin(admin.ModelAdmin):
    class Media:
        pass
        #js = ('js/custom_m2m.js',)
    
    fieldsets = [
        (None, {
            'fields': ('site', ('sku', 'isbn',), ('name', 'slug',), \
            ('publisher', 'pub_date'), 'pages', 'short_desc', 'long_desc', \
            'quantity', 'language', 'category', 'tax', 'options')
        }),
        ('Pricing', {
            'fields': ('price', 'cost', 'special_price', ('spvf', 'spvt'))
        }),
    ]


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ('options',)

class CartShippingInline(admin.TabularInline):
    model = CartShipping

class CartShippingAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline, CartShippingInline,]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('options',)
    extra = 0
    can_delete = False
    readonly_fields = ('qty', 'unit_price', 'content_type', 'object_id', 'options')
    
class OrderNotesInline(admin.TabularInline):
    model = OrderNote
    extra = 1
    exclude = ('created_by',) 
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(OrderNote, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.pk != obj.created_by.pk:
            return False
        return True
        
    def has_delete_permission(self,request,obj=None):
        return self.has_change_permission(request,obj)

class OrderPaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    can_delete = False
    exclude = ('method', 'raw')
    hide_fields = ('method', 'raw', 'created_at', 'updated_at')
    template = 'admin/shop/payment/tabular.html'
        
    def __init__(self, *args, **kwargs):
        super(OrderPaymentInline, self).__init__(*args, **kwargs)
        self.readonly_fields = self.get_display_fields()
        
    def get_display_fields(self):
        fields = []
        for field in self.model._meta.fields:
            if field.name not in self.hide_fields:
                fields.append(field.name)
        return fields


class OrderAdmin(admin.ModelAdmin):
    form = AdminOrderForm
    search_fields = ['customer__username', 'id']
    #raw_id_fields = ('items',)
    inlines = [OrderPaymentInline,]
    list_display = ('id', 'customer', 'status', 'created_at',)
    list_filter = ('status', 'created_at',)
    display_fields = ('status','dealer')
    ordering = ('-created_at',)
    
    def __init__(self, *args, **kwargs):
        super(OrderAdmin, self).__init__(*args, **kwargs)
        self.exclude = self.get_exclude_fields()
        
    def get_exclude_fields(self):
        fields = []
        for field in self.model._meta.fields:
            if field.name not in self.display_fields:
                fields.append(field.name)
        return fields

    def save_formset(self, request, form, formset, change): 
        def set_user(instance):
            if not instance.pk:
                instance.created_by = request.user
                instance.save()

        if formset.model == OrderNote:
            instances = formset.save(commit=False)
            map(set_user, instances)
            formset.save_m2m()
            return instances
        else:
            return formset.save()

    def has_delete_permission(self,request,obj=None):
        if settings.DEBUG:
            return True
        else:
            return False
        
    def change_view(self, request, object_id, extra_context=None):
            my_context = {
                'order': Order.objects.get(pk=object_id),
            }
            return super(OrderAdmin, self).change_view(request, object_id,
                extra_context=my_context)

class TaxRateInline(admin.TabularInline):
    extra = 0
    model = TaxRate
    form = AdminTaxRateForm
    
class TaxClassAdmin(admin.ModelAdmin):
    """docstring for TaxClassAdmin"""
    inlines = [TaxRateInline,]



admin.site.register(Setting)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(TaxClass, TaxClassAdmin)
admin.site.register(Discount)
admin.site.register(Option, OptionAdmin)
admin.site.register(Payment)
admin.site.register(CartShipping, CartShippingAdmin)
