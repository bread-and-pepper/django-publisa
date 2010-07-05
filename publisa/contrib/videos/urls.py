from django.conf.urls.defaults import *

urlpatterns = patterns('videola.views',
    url(r'^upload_progress/$',
        'upload_progress',
        name='upload-progress'),

)
