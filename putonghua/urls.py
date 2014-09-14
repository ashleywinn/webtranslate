from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$',                   'putonghua.views.home_page',        name='home'),
    url(r'search_chinese$',      'putonghua.views.search_chinese',   name='search_chinese'),
    url(r'pinyin/search/(.+)/$', 'putonghua.views.pinyin_search_result', name='pinyin_search_result'),
    url(r'(.+)/english/$',       'putonghua.views.view_english',     name='view_english'),
    url(r'hsk_list/(\d+)/$',     'putonghua.views.view_hsk_list',    name='view_hsk_list'),
    url(r'stats$',          'putonghua.views.view_stats',      name='view_stats'),
)
