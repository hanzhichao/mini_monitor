from django.conf.urls import url, include
from django.contrib import admin
# from django.contrib.auth.models import User
# from rest_framework import routers, serializers, views
from monitor import views
from MiniMonitor.views import homepage, manager

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/apps/$', views.app_list),
    url(r'^api/apps/(?P<pk>[0-9]+)/$', views.app_detail),

    url(r'^api/statistics/(?P<pk>[0-9]+)/$', views.app_statistics_list),

    url(r'^api/app_history/$', views.app_history_list),
    url(r'^api/app_history/(?P<pk>[0-9]+)/$', views.app_history_detail),

    url(r'^api/groups/$', views.group_list),
    url(r'^api/groups/(?P<pk>\d+)/$', views.group_detail),  # api/groups/1/

    url(r'^api/hosts/$', views.host_list),
    url(r'^api/hosts/(?P<pk>[0-9]+)/$', views.host_detail),
    url(r'^api/count/groups/$', views.count_groups),
    url(r'^$', homepage)
]
