from django.conf.urls.defaults import *

urlpatterns = patterns('publisa.views',
    url(r'^tags/$',
        view='tag_list',
        name='publisa-tag-list'),
    url(r'^page/(?P<page>\w)/$',
        view='index',
        name='publisa-index-paginated'),
    url('^$',
       name='publisa-index',
       view='index',)
)
