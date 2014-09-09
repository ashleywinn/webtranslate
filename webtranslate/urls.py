from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$',       'putonghua.views.home_page', name='home'),
    url(r'^reader/', include('putonghua.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
