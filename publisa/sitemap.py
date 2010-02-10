from django.contrib.sitemaps import Sitemap
from publisa.models import Publish

class PublishSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Publish.objects.published()

    def lastmod(self, obj):
        return obj.publish
