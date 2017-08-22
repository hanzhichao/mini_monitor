"""MiniMonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
# from django.contrib.auth.models import User
# from rest_framework import routers, serializers, views
from monitor import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/apps/$',views.app_list),
    url(r'^api/apps/(?P<pk>[0-9]+)/$',views.app_detail),

    url(r'^api/app_statistics/$',views.app_statistics_list), 
    url(r'^api/app_statistics/(?P<pk>[0-9]+)/$',views.app_statistics_detail),

    url(r'^api/app_history/$',views.app_history_list),
    url(r'^api/app_history/(?P<pk>[0-9]+)/$',views.app_history_detail),

    url(r'^api/groups/$',views.group_list),
    url(r'^api/groups/(?P<pk>[0-9]+)/$',views.group_detail),

    url(r'^api/hosts/$',views.host_list), 
    url(r'^api/hosts/(?P<pk>[0-9]+)/$',views.host_detail)
]
