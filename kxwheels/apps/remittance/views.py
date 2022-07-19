# TODO:add request.session[settings.CACHE_GATEWAY_KEY] to the context
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.models import User

from django.conf import settings as global_settings

from kxwheels.apps.remittance.conf import settings
from kxwheels.apps.remittance.forms import PaymentForm, PayPalForm
from kxwheels.apps.remittance.decorators import require_gateway
from django.core.mail import send_mail
from kxwheels.context_processors import get_subdomain_owner
from kxwheels.apps.shop.conf import settings as shop_settings

TRANS_KEY = settings.SESSION_TRANSACTION_KEY
CACHE_KEY = settings.CACHE_GATEWAY_KEY

class PaymentCancelView(TemplateView):
    template_name = 'remittance/payment_cancel.html'

    def get(self, request, *args, **kwargs):
        # TODO: This should remain in Shop app
        # Remove order from session
        from kxwheels.apps.shop.conf import settings as shop_settings
        try:
            del(request.session[shop_settings.ORDER_SESSION_KEY])
        except KeyError:
            pass
        return HttpResponseRedirect('/')

class PaymentProcessView(TemplateView):
    template_name = 'remittance/payment_processing.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST',])

    @method_decorator(require_gateway)
    def post(self, request, *args, **kwargs):
        """
        Handles the post request from the final payment confirmation
        page with payment information as a request.
        """
        context = self.get_context_data(**kwargs)
        gateway = cache.get(request.session['gateway'])

        form = PaymentForm(request.POST)
        if form.is_valid():
            transaction = gateway.get_response(form)


            transaction_key = 'transaction-{}'.format(transaction.trans_id)
            cache.set(transaction_key, transaction)
            request.session[TRANS_KEY] = transaction_key

            if transaction.is_success:
                return HttpResponseRedirect(
                    reverse("remittance_payment_success"))
            else:
                messages.add_message(request, messages.ERROR,
                                     transaction.message)
                return HttpResponseRedirect(
                    reverse('remittance_payment_failure'))
        else:
            print '--------------'
            raise Exception('INVALID PAYMENT FORM')

        context["form"] = form
        context["gateway"] = gateway
        return self.render_to_response(context)


class PaypalProcessView(TemplateView):
    template_name = 'remittance/payment_success.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST',])

    @method_decorator(require_gateway)
    def post(self, request, *args, **kwargs):
        """
        Handles the post request from the final payment confirmation
        page with paypal information as a request.
        """
        context = self.get_context_data(**kwargs)
        gateway = cache.get(request.session['gateway'])

        form = PayPalForm(request.POST)
        if form.is_valid():
            context['paypal'] = True
            context['paypal_email'] = form.cleaned_data['notes']
            context['order'] = request.session[shop_settings.ORDER_SESSION_KEY]
        else:
            messages.add_message(request, messages.ERROR,
                                 _("Enter a Valid Paypal Email!"))
            return HttpResponseRedirect(reverse('remittance_payment_failure'))

        # Remove order from session
        try:
            del(request.session[shop_settings.ORDER_SESSION_KEY])
        except KeyError:
            pass

        recipients = ['benny@countable.ca', global_settings.ADMIN_EMAIL]
        subdomain_owner = get_subdomain_owner(request)
        if subdomain_owner:
          recipients.append(subdomain_owner.email)

        # send_mail('New PayPal Order %s'%context['order'], 'Someone placed a paypal order with paypal email: %s.'%context['paypal_email'], 'mailer@kxwheels.com', recipients, fail_silently=False)

        return self.render_to_response(context)


class PaymentSuccessView(TemplateView):
    template_name = 'remittance/payment_success.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        transaction = cache.get(request.session.get(TRANS_KEY, None))

        if transaction is not None:
            context['transaction'] = transaction
            context['purchase'] = transaction.purchase
            context['seller'] = transaction.purchase.seller
            context['buyer'] = transaction.purchase.buyer
            context['paypal'] = False
        else:
            messages.add_message(request, messages.ERROR,
                                 _("Transaction does not exist in Session"))
            return HttpResponseRedirect(reverse('remittance_payment_failure'))

        # TODO: This should remain in Shop app
        # Remove order from session
        try:
            del(request.session[shop_settings.ORDER_SESSION_KEY])
        except KeyError:
            pass

        recipients = [global_settings.ADMIN_EMAIL]
        subdomain_owner = get_subdomain_owner(request)
        if subdomain_owner:
          recipients.append(subdomain_owner.email)

        send_mail('New Order %s.'%transaction.purchase.order,
                  'Someone placed an order %s.'%transaction.purchase.order,
                  'mailer@kxwheels.com',
                  recipients, fail_silently=False)
        return self.render_to_response(context)

class PaymentFailureView(TemplateView):
    template_name = 'remittance/payment_failure.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        transaction = cache.get(request.session.get(TRANS_KEY, None))

        if transaction is None:
            messages.add_message(request, messages.ERROR,
                                 _("Transaction does not exist in Session"))

        context['transaction'] = transaction
        return self.render_to_response(context)

class PurchaseView(TemplateView):
    template_name = "remittance/purchase_detail.html"
    context_object_name = 'purchase'


    @method_decorator(require_gateway)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        gateway = cache.get(request.session['gateway'])
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)

        context['seller'] = gateway.seller
        context['buyer'] = gateway.buyer
        context['purchase'] = gateway.purchase
        context['purchase_items'] = gateway.purchase_items

        return self.render_to_response(context)