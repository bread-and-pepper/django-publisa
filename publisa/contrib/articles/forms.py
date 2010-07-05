from django import forms
from django.forms import widgets
from django.db import models
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from artikelly import settings as art_settings

from artikelly.models import Article, InlineType

def get_inline_form(inline_model):
    class _InlineForm(forms.ModelForm):
        class Meta:
            model = inline_model
    return _InlineForm

class InlineTypeWidget(widgets.Select):
    def render(self, name, value, attrs=None, choices=()):
        context = {'choices': self.choices,
                   'classes': art_settings.ARTIKELLY_PHOTO_CLASSES}
        return render_to_string('admin/inlines/widget.html', context)

class ArticleAdminForm(forms.ModelForm):
    inline = forms.ModelChoiceField(InlineType.objects.all(),
                                    widget=InlineTypeWidget,
                                    required=False)


    class Media:
        js = ('artikelly/js/kelly.ui.js',)
        css = {
            'all': ('artikelly/css/admin_inline.css',)
        }


    class Meta:
        model = Article
