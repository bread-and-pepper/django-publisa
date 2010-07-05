from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from columnadia.models import Columnist

class ColumnistForm(forms.ModelForm):
    first_name = forms.CharField(max_length=256, label=_('First name'))
    last_name = forms.CharField(max_length=256, label=_('Last name'))

    def __init__(self, *args, **kwargs):
        super(ColumnistForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        fields = ['first_name', 'last_name', 'user', 'headshot', 'annotation', 'biography']
