from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from artikelly.models import Article, InlineType, Photo, Category
from artikelly.forms import ArticleAdminForm
from artikelly.widgets import AdminThumbWidget

from markitup.widgets import MarkItUpWidget

class ArticleAdmin(admin.ModelAdmin):

    def author_full(self, obj):
        return ("%s" % (obj.author.get_full_name()))
    author_full.short_description = _('Author')

    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'author_full', 'status')
    list_filter = ('status',)
    form = ArticleAdminForm
    exclude = ('body_html', 'teaser_html')

    formfield_overrides = {
        models.TextField: {'widget': MarkItUpWidget},
    }

    def redirect_to_publish(self, obj):
        """ Redirect to publisa """
        if obj.status != 2:
            obj.status = 2
            obj.save()
        return reverse('admin:publisa_publish_change', args=(obj.publish.pk, ))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
        return super(ArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def response_add(self, request, obj):
        result = super(ArticleAdmin, self).response_add(request, obj)

        if request.POST.has_key('_publish'):
            result['Location'] = self.redirect_to_publish(obj)
        return result

    def response_change(self, request, obj):
        result = super(ArticleAdmin, self).response_change(request, obj)

        if request.POST.has_key('_publish'):
            result['Location'] = self.redirect_to_publish(obj)
        return result

class PhotoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': AdminThumbWidget},
    }

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js',
              'artikelly/js/jquery.fancybox-1.2.6.pack.js',
              'artikelly/js/kelly.ui.js')

        css = {'all': ('artikelly/css/jquery.fancybox-1.2.6.css',) }

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(InlineType)
admin.site.register(Category, CategoryAdmin)
