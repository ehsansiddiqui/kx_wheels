from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from kxwheels.apps.account.models import Profile, Dealer, Developer
from kxwheels.apps.account.forms import ProfileAdminForm
from kxwheels.apps.kx.models.tire import TireManufacturerDiscount, DealerTireManufacturerDiscount
from kxwheels.apps.kx.models.wheel import WheelManufacturerDiscount, DealerWheelManufacturerDiscount
from kxwheels.apps.shop.models import Order

admin.site.unregister(User)

class TireManufacturerDiscountInline(admin.TabularInline):
    model = TireManufacturerDiscount
    extra = 10

class WheelManufacturerDiscountInline(admin.TabularInline):
    model = WheelManufacturerDiscount
    extra = 10

class DealerTireManufacturerDiscountInline(admin.TabularInline):
    model = DealerTireManufacturerDiscount
    extra = 10

class DealerWheelManufacturerDiscountInline(admin.TabularInline):
    model = DealerWheelManufacturerDiscount
    extra = 10

class ProfileInline(admin.StackedInline):
    model = Profile
    form = ProfileAdminForm

class UserAdmin(BaseUserAdmin):
    change_list_template = 'admin/dealer_list.html'
    inlines = (ProfileInline,TireManufacturerDiscountInline,WheelManufacturerDiscountInline,)
    list_display = BaseUserAdmin.list_display + ('dealer',)
    def dealer(self, user):
        orders = Order.objects.filter(customer=user,dealer__isnull=False)
        if len(orders):
            return orders[0].dealer
    #list_filter = ('profiles__subdomain__isnull',)
    
from django.contrib.auth.models import User

admin.site.register(User, UserAdmin)
admin.site.register(Dealer, readonly_fields = ('created_at',))
admin.site.register(Developer)
