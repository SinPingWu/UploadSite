from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^upload/page/$', views.upload_app_page),
    url(r'^upload/$', views.upload_app),
    url(r'^download/$', views.download_app),
    url(r'^list/$', views.app_list),
    url(r'^update/info/$', views.get_update_info),
]