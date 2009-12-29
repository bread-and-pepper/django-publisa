from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from publisa.models import Publish

class PublishAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'content_object', 'published_humanised', 'banner')
    list_filter = ('publish', 'banner')

    def change_view(self, request, object_id, extra_context=None):
        publish = Publish.objects.get(pk=object_id)
        # If the item has ``admin_preview`` enabled. Supply the view with the
        # published item
        print publish.content_object.admin_preview
        if publish.content_object.admin_preview:
            my_context = {'item': publish}
        else: my_context = None

        return super(PublishAdmin, self).change_view(request,
                                                     object_id,
                                                     extra_context=my_context)

    def get_form(self, request, obj=None, **kwargs):
        if obj and not obj.content_object.allow_banners:
            self.exclude = ('banner',)
        return super(PublishAdmin, self).get_form(request, obj=None, **kwargs)

admin.site.register(Publish, PublishAdmin)
