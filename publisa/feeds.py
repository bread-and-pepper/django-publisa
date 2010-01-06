from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from publisa.models import Publish

class PublishFeed(Feed):
    _site = Site.objects.get_current()
    title = '%s feed' % _site.name
    description = '%s publish feed.' % _site.name

    def link(self):
        return reverse('publisa-index')

    def items(self):
        return Publish.objects.published()[:10]

    def item_pubdate(self, obj):
        return obj.publish
    
