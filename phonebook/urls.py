from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.contrib.auth.views import login, logout_then_login
from phones import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.list, name='list'),
    url(r'^list/$', views.list, name='list'),
    url(r'^view/(?P<id_record>\d+)/$', views.view_record, name='view_record'),
    url(r'^delete/$', views.delete_records, name='delete'),
    url(r'^new_record/$', views.new_record, name='new_record'),
    url(r'^accounts/login/$', login, {'template_name': 'phones/login.html'}),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^new_user/$', views.new_user, name='new_user'),
    url(r'^only_view/(?P<id_record>\d+)/$', views.only_view, name='only_view'),
    # url(r'^phonebook/', include('phonebook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
