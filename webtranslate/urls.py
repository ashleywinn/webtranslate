from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$',              'putonghua.views.home_page',       name='home'),
    url(r'^putonghua/new_chinese$', 
                            'putonghua.views.new_chinese',     name='new_chinese'),
    url(r'^english/(.+)/$', 'putonghua.views.view_english',    name='view_english'),
    url(r'^english/(.+)/new_translation$', 
                            'putonghua.views.new_translation', name='new_translation'),
    url(r'^english/(.+)/new_pinyin$', 
                            'putonghua.views.new_pinyin',      name='new_pinyin'),

    url(r'^admin/', include(admin.site.urls)),
)
