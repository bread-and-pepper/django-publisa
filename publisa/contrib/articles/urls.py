from django.conf.urls.defaults import *

urlpatterns = patterns('artikelly.views',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        name='artikelly-detail',
        view='detail',
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        view='archive_day',
        name='artikelly-archive-day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        view='archive_month',
        name='artikelly-archive-month'
    ),
    url(r'^(?P<year>\d{4})/$',
        view='archive_year',
        name='artikelly-archive-year'
    ),
    url(r'^categories/(?P<slug>[-\w]+)/page/(?P<page>\d)/$',
        view='category_detail',
        name='artikelly-category-detail-paginated'
    ),
    url(r'^categories/(?P<slug>[-\w]+)/$',
        view='category_detail',
        name='artikelly-category-detail'
    ),
    url (r'^categories/$',
        view='category_list',
        name='artikelly-category-list'
    ),
    url(r'^admin/inline/(?P<inline_id>\d+)/$',
        name='artikelly-admin-inline',
        view='admin_inline'),
    url(r'^page/(?P<page>\d)/$',
        view='list',
        name='artikelly-list-paginated'),
    url(r'^$',
        name='artikelly-list',
        view='list'),
)
