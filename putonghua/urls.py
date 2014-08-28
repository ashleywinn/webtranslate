from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$',               'putonghua.views.home_page',       name='home'),
    url(r'new_chinese$',     'putonghua.views.new_chinese',     name='new_chinese'),
    url(r'(.+)/english/$',   'putonghua.views.view_english',    name='view_english'),
    url(r'hsk_list/(\d+)/$', 'putonghua.views.view_hsk_list',    name='view_hsk_list'),
    url(r'(.+)/new_translation$', 
                              'putonghua.views.new_translation', name='new_translation'),
    url(r'(.+)/new_pinyin$', 
                              'putonghua.views.new_pinyin',      name='new_pinyin'),
)
