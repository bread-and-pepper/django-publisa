from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings

import os

class AdminThumbWidget(forms.FileInput):
    """
    A Image FileField Widget that shows a thumbnail if it has one.
    """
    def __init__(self, attrs={}):
        super(AdminThumbWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            try:
                from sorl.thumbnail.main import DjangoThumbnail
                thumb = '<img src="%s" style="float:left; margin-right: 10px; border: 1px solid #333;">' % DjangoThumbnail(value.name, (80,80), ['crop']).absolute_url
            except:
                # just act like a normal file
                output.append('%s <a href="%s">%s</a> <br />%s ' %
                    (_('Currently:'), value.url, os.path.basename(value.path), _('Change:')))
            else:
                output.append('<a class="thumb" href="%s">%s</a>%s ' %
                    (value.url, thumb, _('Change:')))
        output.append(super(AdminThumbWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
