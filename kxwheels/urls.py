"""kxwheels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
import kxwheels.apps.search.views
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include



Imageslider = kxwheels.apps.search.views.ImageSliders.as_view()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content/', include('django.contrib.flatpages.urls')),
    url(r'^search/', include('kxwheels.apps.search.urls')),
    url(r'^account/', include('kxwheels.apps.account.urls')),
    url(r'^shop/', include('kxwheels.apps.shop.urls')),
    url(r'^remittance/', include('kxwheels.apps.remittance.urls')),
    url(r'^kx/', include('kxwheels.apps.kx.urls')),
    url(r'^vehicle/', include('kxwheels.apps.vehicle.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),

    # url(r'^iconfig/$', direct_to_template, {'template': 'iconfig.html'}, name="iconfig"),
    # url(r'^robots.txt', direct_to_template, {'template': 'robots.txt'}, name="robots.txt"),
    url(r'^$', Imageslider, name="homepage"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()