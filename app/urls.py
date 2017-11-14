from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^list/$', views.app_list),
    url(r'^update/page/$', views.update_app_page),
    url(r'^update/$', views.upload_app),
    url(r'^download/$', views.download_app),
    url(r'^list/$', views.app_list),
    url(r'^update/info/$', views.get_update_info),
    url(r'^add/$', views.app_add),
    url(r'^add/page/$', views.app_add_page),
]