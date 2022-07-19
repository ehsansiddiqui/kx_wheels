import os
import time
import uuid
import logging
import datetime
from urllib import urlencode

from collections import OrderedDict

from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (TemplateView, DetailView, ListView)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from haystack.query import SQ, SearchQuerySet

from kxwheels.apps.kx.models.accessories import *
from kxwheels.apps.kx.tasks import import_wheels
from kxwheels.apps.kx.forms import WheelSizeSearchForm, VehicleSearch, WheelReviewForm, WheelCustomerMediaForm
from kxwheels.apps.kx.utils import cut_decimals

from kxwheels.apps.vehicle.models import Model

# Temporary imports
from django.http import HttpResponse

logger = logging.getLogger('project.navdeep')


class KxAccessories(TemplateView):
    template_name = 'kx/accessories/accessories.html'
    model = Accessories

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        accessories = Accessories.objects.all()
        context['accessories'] = accessories

        return self.render_to_response(context)


class KxAccessoriesListView(ListView):
    model = AccessoriesList
    paginate_by = 25
    context_object_name = 'accessories_list'
    template_name = "kx/accessories/accessories_list.html"

    def get_queryset(self):
        self.accessories = get_object_or_404(Accessories, slug=self.kwargs['slug'])
        return AccessoriesList.objects.filter(manufacturer=self.accessories)

    def get_context_data(self, **kwargs):
        context = super(KxAccessoriesListView, self).get_context_data(**kwargs)
        context['accessories'] = self.accessories
        return context


class KxAccessoriesDetailView(DetailView):
    context_object_name = 'accessories'
    queryset = AccessoriesList.objects.all()
    template_name = "kx/accessories/accessories_detail.html"

    def get_context_data(self, **kwargs):
        context = super(KxAccessoriesDetailView, self).get_context_data(**kwargs)
        wheelsize_pk = self.request.GET.get('s', None)
        if wheelsize_pk and wheelsize_pk != 'undefined':
            self.wheelsize = get_object_or_404(AccessoriesDetail, pk=wheelsize_pk)
            context['wheelsize'] = self.wheelsize

        wheel = self.get_object()

        # Reviews
        reviews = AccessoriesReview.approved.filter(reviewee=wheel)

        context['reviews'] = reviews

        # Customer media
        customer_media = AccessoriesCustomerMedia.active.filter(accessorie=wheel)
        context['customer_media'] = customer_media
        context['auth_and_active_user'] = self.request.user.is_authenticated()
        return context
