from django.conf.urls.defaults import *

urlpatterns = patterns('publisa.views',
   url('^$',
       name='publisa-index',
       view='index',)
)
