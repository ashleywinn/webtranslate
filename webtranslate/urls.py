from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$',              'putonghua.views.home_page',       name='home'),
    url(r'^putonghua/new_translation$', 
                            'putonghua.views.new_translation', name='new_translation'),
    url(r'^english/(.+)/$', 'putonghua.views.view_english',    name='view_english'),

    url(r'^admin/', include(admin.site.urls)),
)
