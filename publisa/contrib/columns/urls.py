from django.conf.urls.defaults import *

urlpatterns = patterns('columnadia.views',
    url(r'^(?P<columnist>[-\w]+)/(?P<column>[-\w]+)/$',
        view='column_detail',
        name='columnadia-column-detail'),
    url(r'^(?P<columnist>[-\w]+)/$',
        view='columnist_detail',
        name='columnadia-columnist-detail'),
    url(r'^$',
        view='index',
        name='columnadia-index'),
)
