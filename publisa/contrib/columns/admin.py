from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify

from columnadia.models import Column, Columnist
from columnadia.forms import ColumnistForm

from markitup.widgets import MarkItUpWidget

class ColumnAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {'widget': MarkItUpWidget},
    }

class ColumnistAdmin(admin.ModelAdmin):
    form = ColumnistForm

    def save_model(self, request, obj, form, change):
        obj.user.first_name = form.cleaned_data['first_name']
        obj.user.last_name = form.cleaned_data['last_name']
        obj.user.save()
        obj.slug = slugify(obj.user.get_full_name())
        obj.save()

admin.site.register(Column, ColumnAdmin)
admin.site.register(Columnist, ColumnistAdmin)
