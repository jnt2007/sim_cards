# -*- coding: utf-8 -*-
"""sims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
from sim_page import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.power_master, name='power_master'),
    url(r'^pmaster/', views.power_master, name='power_master'),
    url(r'^pmanage/', views.power_manage, name='power_manage'),
    url(r'^dev/', views.dev, name='dev'),
    url(r'^alpha/', views.alpha, name='alpha'),
    url(r'^save_info?$', views.save_info),
    url(r'^update_balance?$', views.schedule_balance_renewal)
]
#  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

