from django.views.generic import list_detail

from publisa import settings as publisa_settings
from publisa.models import Publish

def index(request, page=0):
    """ Returns a list of articles """
    return list_detail.object_list(request,
                                   queryset=Publish.objects.published(),
                                   page=page,
                                   paginate_by=publisa_settings.PUBLISA_PAGINATE_BY,
                                   template_object_name='publish')
