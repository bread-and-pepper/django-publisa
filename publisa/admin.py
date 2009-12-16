from django.contrib import admin
from django.utils.translation import ugettext as _

from publisa.models import Publish
from publisa.forms import PublishAdminForm

class PublishAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'content_object', 'published_humanised', 'banner')
    list_filter = ('publish', 'banner')

    def get_form(self, request, obj=None, **kwargs):
        if obj and not obj.child().allow_banners:
            self.exclude = ('banner',)
        return super(PublishAdmin, self).get_form(request, obj=None, **kwargs)

admin.site.register(Publish, PublishAdmin)
