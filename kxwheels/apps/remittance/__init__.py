# #TODO: Implement cleanup for dormant purchases
import sys
# import uuid
# from django.core.cache import cache
# from django.core.urlresolvers import reverse
# from django.forms.models import model_to_dict
# from django.http import HttpResponse, HttpResponseRedirect
from .conf import settings
# from .models import Seller, Buyer, Purchase, PurchaseItem
#
def get_module(module_name=settings.REMITTANCE_MODULE):
    if not module_name in settings.REMITTANCE_MODULE:
        # Raise module does not exist
        return False

    try:
        module = sys.modules['kxwheels.apps.remittance.modules.%s' % module_name]
    except KeyError:
        __import__('kxwheels.apps.remittance.modules.%s' % module_name)
        module = sys.modules['kxwheels.apps.remittance.modules.%s' % module_name]
    return module
#
#
# def Emption(request, seller, buyer, purchase, purchase_items):
#
#     try:
#         purchase = Purchase.objects.get(order=purchase.order)
#     except Purchase.DoesNotExist:
#         pass
#
#     # make data persistent
#
#     # Seller
#     seller_dict = model_to_dict(seller, exclude=['id'])
#     seller, created = Seller.objects.get_or_create(**seller_dict)
#     if created:
#         seller.save()
#
#     # Buyer
#     buyer.save()
#
#     # Purchase
#     purchase.seller = seller
#     purchase.buyer = buyer
#     purchase.save()
#
#     # Purchase item(s)
#     for item in purchase_items:
#         try:
#             purchase_item = PurchaseItem.objects.get(purchase=purchase, sku=item.sku)
#         except PurchaseItem.DoesNotExist:
#             item.purchase = purchase
#             item.save()
#
#     payment_module = get_module()
#     gateway = payment_module.Emption(
#         seller=seller,
#         buyer=buyer,
#         purchase=purchase,
#         purchase_items=purchase_items
#     )
#
#     gateway_key = 'gateway-{}'.format(gateway.id)
#     cache.set(gateway_key, gateway)
#     request.session['gateway'] = gateway_key
#
#     return HttpResponseRedirect(reverse('remittance_purchase_detail',
#                                         args=[gateway.purchase.order]))
#
# def PreAuth(seller, buyer, purchase, purchase_items):
#     payment_module = get_module()
#     gateway = payment_module.PreAuth(
#         seller=seller,
#         buyer=buyer,
#         purchase=purchase,
#         purchase_items=purchase_items
#     )
#     # `get_response` function should return the url to the appropriate page
#     return gateway.get_response()
#
# def Capture(order_id, trans_id, amount):
#     payment_module = get_module()
#     try:
#         gateway = payment_module.Capture(order_id=order_id, trans_id=trans_id, amount=amount)
#     except AttributeError:
#         return HttpResponse('This module does not allow capturing transactions via the API')
#     else:
#         # `get_response` function should return the url to the appropriate page
#         return gateway.get_response()
