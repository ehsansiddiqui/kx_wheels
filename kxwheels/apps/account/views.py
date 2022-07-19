import os
import json
import requests
import hashlib
import StringIO
import xlsxwriter
import io

from pandas import DataFrame
from xlsxwriter.workbook import Workbook

from django.contrib.auth import authenticate, login
import re
from django.core.files.storage import default_storage
from kxwheels import context_processors
from django.template.loader import render_to_string
from django.shortcuts import render
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import (HttpResponse)
from django.utils.decorators import method_decorator
from django.views.generic import (TemplateView, DetailView, ListView, UpdateView, CreateView, DeleteView)
from registration.views import RegistrationView as BaseRegistrationView

from kxwheels.apps.account.forms import ProfileForm, DealerForm, RegistrationFormNoUserName
from kxwheels.apps.account.models import Profile, Dealer
from kxwheels.apps.kx.models.tire import DealerTireManufacturerDiscount, TireManufacturer
from kxwheels.apps.kx.models.wheel import DealerWheelManufacturerDiscount, WheelManufacturer
from kxwheels.apps.kx.utils import extract_subdomain
from kxwheels.apps.shop.models.order import Order
from kxwheels.apps.shop.models.cart import OrderLogout
from kxwheels.apps.account.models import User
from kxwheels.apps.shop.models.cart import OrderLogoutProductt
from kxwheels.settings.base import *
from kxwheels.apps.shop.models.order import OrderLoginProduct



class LoginView(TemplateView):
    model = User
    template_name = "account/login.html"

    def post(self, request, *args, **kwargs):
        email =  request.POST['email']
        password =  request.POST['password']
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(86400)
                    login(request, user)

                return redirect('/')
            else:
                context = {'error': 'Wrong Email or Password',}
                return HttpResponse(render_to_string(request=request,
                                                     template_name=self.template_name,
                                                     context=context))
        except Exception as e:

            context = {'error': 'Wrong Email or Password',}
            return HttpResponse(render_to_string(request=request,
                                                 template_name=self.template_name,
                                                 context=context))




class RegistrationView(BaseRegistrationView):
    form_class = RegistrationFormNoUserName


    def get_success_url(self, user):
        return reverse("auth_login")

    def register(self, form):
        user = form.save()
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        return user


class AccountView(TemplateView):
    template_name = "account/account.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            shipping_profile = Profile.objects.get(user=request.user, name="shipping")
        except Profile.DoesNotExist, e:
            shipping_profile = None

        try:
            billing_profile = Profile.objects.get(user=request.user, name="billing")
        except Profile.DoesNotExist, e:
            billing_profile = None

        context['shipping_profile'] = shipping_profile
        context['billing_profile'] = billing_profile
        context['user'] = request.user

        return self.render_to_response(context)


class DealerOrderListView(TemplateView):
    template_name = "account/dealer_orders.html"

    def get(self, request, *args, **kwargs):
        subdomain, subdomain_profile = extract_subdomain(request)
        if subdomain and request.user != subdomain_profile.user:
            return HttpResponse("Only dealer can view the orders.")

        context = self.get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(dealer=request.user).order_by('-created_at')

        return self.render_to_response(context)

def generate_missing_markups(u, context):
    ''' Create any markups not defined for any particular manufacturer, for this user. '''
    tire_markups = DealerTireManufacturerDiscount.objects.filter(user=u)
    wheel_markups = DealerWheelManufacturerDiscount.objects.filter(user=u)
    for m in context['tire_manufacturer_list']:
        markups = [a for a in tire_markups if a.manufacturer==m]
        if not len(markups):
            d = DealerTireManufacturerDiscount(
                user=u,
                manufacturer=m,
                discount=25
            )
            d.save()

    for m in context['wheel_manufacturer_list']:
        markups = [a for a in wheel_markups if a.manufacturer==m]
        if not len(markups):
            d = DealerWheelManufacturerDiscount(
                user=u,
                manufacturer=m,
                discount=25
            )
            d.save()



class DealerManufacturerDiscountsView(TemplateView):
    template_name = "account/dealer_manufacturer_discounts.html"

    def get(self, request, *args, **kwargs):
        subdomain, subdomain_profile = extract_subdomain(request)
        if subdomain and request.user != subdomain_profile.user:
            return HttpResponse("Only dealer can edit the markups.")
        context = self.get_context_data(**kwargs)
        context['tire_manufacturer_list'] = TireManufacturer.objects.visible()
        context['wheel_manufacturer_list'] = WheelManufacturer.objects.visible()
        generate_missing_markups(request.user, context)
        context['dealer_tire_manufacturer_discounts'] = [dmd for dmd in DealerTireManufacturerDiscount.objects.filter(user=request.user).order_by('manufacturer__name') if dmd.manufacturer in context['tire_manufacturer_list']]
        context['dealer_wheel_manufacturer_discounts'] = [dmd for dmd in DealerWheelManufacturerDiscount.objects.filter(user=request.user).order_by('manufacturer__name') if dmd.manufacturer in context['wheel_manufacturer_list']]
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        errors = []
        tire_discounts = {}
        wheel_discounts = {}
        if request.POST.has_key('tire_manufacturers'):
            for m in request.POST.getlist('tire_manufacturers'):
                if m != '-1' and request.POST.has_key('tire_discount_' + m):
                    tire_discount = request.POST['tire_discount_' + m]
                    if not re.match(r'^\d+$', tire_discount):
                        errors.append('Invalid Discount')
                        break
                    tire_discounts[m] = tire_discount
        if not errors:
            if request.POST.has_key('wheel_manufacturers'):
                for m in request.POST.getlist('wheel_manufacturers'):
                    if m != '-1' and request.POST.has_key('wheel_discount_' + m):
                        wheel_discount = request.POST['wheel_discount_' + m]
                        if not re.match(r'^\d+$', wheel_discount):
                            errors.append('Invalid Discount')
                            break
                        wheel_discounts[m] = wheel_discount

        if not errors:
            DealerTireManufacturerDiscount.objects.filter(user=request.user).delete()
            for m_id, discount in tire_discounts.items():
                DealerTireManufacturerDiscount(user=request.user,manufacturer=TireManufacturer.objects.get(id=int(m_id)),discount=int(discount)).save()
            DealerWheelManufacturerDiscount.objects.filter(user=request.user).delete()
            for m_id, discount in wheel_discounts.items():
                DealerWheelManufacturerDiscount(user=request.user,manufacturer=WheelManufacturer.objects.get(id=int(m_id)),discount=int(discount)).save()

        context['tire_manufacturer_list'] = TireManufacturer.objects.visible()
        context['wheel_manufacturer_list'] = WheelManufacturer.objects.visible()
        context['dealer_tire_manufacturer_discounts'] = [dmd for dmd in DealerTireManufacturerDiscount.objects.filter(user=request.user).order_by('manufacturer__name') if dmd.manufacturer in context['tire_manufacturer_list']]
        context['dealer_wheel_manufacturer_discounts'] = [dmd for dmd in DealerWheelManufacturerDiscount.objects.filter(user=request.user).order_by('manufacturer__name') if dmd.manufacturer in context['wheel_manufacturer_list']]
        context['errors'] = errors
        return self.render_to_response(context)

# Olde
class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        obj = context[list(context)[0]]
        dictionary = {}
        for field in obj._meta.get_all_field_names():
            dictionary[field] = str(obj.__getattribute__(field))
        return json.dumps(dictionary)

# Customer Profile
class ProfileMixin(object):
    model = Profile
    form_class = ProfileForm
    slug_field = 'name'


class UsersProfileMixin(ProfileMixin):
    def get_queryset(self):
        return super(ProfileMixin, self).get_queryset().filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersProfileMixin, self).dispatch(*args, **kwargs)



class ProfileDetailView(UsersProfileMixin, JSONResponseMixin, DetailView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        else:
            return DetailView.render_to_response(self, context)



class ProfileListView(UsersProfileMixin, ListView):
    pass



class ProfileCreateView(UsersProfileMixin, CreateView):
    def get_success_url(self):
        return reverse('auth_account')

    def get_form(self, *args, **kwargs):
        form = super(UsersProfileMixin, self).get_form(*args, **kwargs)
        form.instance = self.model(
            user=self.request.user,
            site=Site.objects.get_current(),
            name=self.kwargs.get('slug'),
        )
        return form

    def get_context_data(self, **kwargs):
        context = super(ProfileCreateView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context



class ProfileUpdateView(UsersProfileMixin, UpdateView):
    def get_success_url(self):
        return reverse('auth_account')

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context



class ProfileDeleteView(UsersProfileMixin, DeleteView):
    def get_success_url(self):
        return reverse('auth_account')



# Dealer
class DealerCreateView(CreateView):
    model = Dealer
    form_class = DealerForm

    def get_success_url(self):
        return reverse('auth_dealer_create_thanks')


    '''
    def form_valid(self, form):
        pass
    '''

class DealerCreateDownloadView(CreateView):
    def get(self, request, *args, **kwargs):

        output = io.BytesIO()
        i = 0
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'Here Is the Complete data of Dealers Information in Kxwheels', bold)
        worksheet.write('A3', 'Dealer ID', bold)
        worksheet.write('B3', 'Business Name', bold)
        worksheet.write('C3', 'Contact Name', bold)
        worksheet.write('D3', 'Street Address', bold)
        worksheet.write('E3', 'City', bold)
        worksheet.write('F3', 'Postal Code', bold)
        worksheet.write('G3', 'Province', bold)
        worksheet.write('H3', 'Country', bold)
        worksheet.write('I3', 'Email', bold)
        worksheet.write('J3', 'Business Phone', bold)
        worksheet.write('K3', 'Other Phone', bold)
        worksheet.write('L3', 'Heard About Us', bold)
        worksheet.write('M3', 'Business Kind', bold)
        worksheet.write('N3', 'Business Kind Other', bold)
        worksheet.write('O3', 'Interested In', bold)
        worksheet.write('P3', 'Volume', bold)
        worksheet.write('Q3', 'Comments', bold)
        worksheet.write('R3', 'Created At', bold)

        dealers_data = Dealer.objects.all().order_by('id')
        for dealer in dealers_data:
            date = str(dealer.created_at).split('.')
            row = i + 4
            worksheet.write(row, 0, dealer.id)
            worksheet.write(row, 1, dealer.business_name)
            worksheet.write(row, 2, dealer.contact_name)
            worksheet.write(row, 3, dealer.street_address)
            worksheet.write(row, 4, dealer.city)
            worksheet.write(row, 5, dealer.postal_code)
            worksheet.write(row, 6, dealer.province)
            worksheet.write(row, 7, dealer.country)
            worksheet.write(row, 8, dealer.email)
            worksheet.write(row, 9, dealer.business_phone)
            worksheet.write(row, 10, dealer.other_phone)
            worksheet.write(row, 11, dealer.heard)
            worksheet.write(row, 12, dealer.business_kind)
            worksheet.write(row, 13, dealer.business_kind_other)
            worksheet.write(row, 14, dealer.interested_in)
            worksheet.write(row, 15, dealer.volume)
            worksheet.write(row, 16, dealer.comments)
            worksheet.write(row, 17, str(date[0]))
            i = i + 1
        workbook.close()

        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Dealers_List.xlsx"

        return response


#vikrant@shiftonline.com
class DealerCreateThanksView(TemplateView):
    template_name = "account/dealer_create_thanks.html"

    def get(self, request, *args, **kwargs):
        try:
            send_mail('mail on wheels','Dealer Registered on Kxwheels.', settings.EMAIL_HOST_USER, ['wdeveloper12@gmail.com'], )
        except  Exception as e:
            print '############################################123'
            print e
            print '############################################123'
        #send_mail('Dealer Inquiry', 'Someone submitted a dealer registeration form.', 'mailer@kxwheels.com', ['kxwheels.com'], fail_silently=False)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)




# Order
class OrderHistoryView(TemplateView):
    template_name = "account/order_history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['orders'] = request.user.orders.all().order_by('-created_at')
        context['ordersproduct'] = OrderLoginProduct.objects.all()
        return self.render_to_response(context)


class OrderHistoryLogoutView(TemplateView):
    model = OrderLogout
    template_name = "account/order_history_logout.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['orders'] = OrderLogout.objects.all().order_by('cart_id')
        context['ordersproduct'] = OrderLogoutProductt.objects.all()

        # context['orders'] = request.user.orders.all().order_by('-created_at')
        return self.render_to_response(context)
