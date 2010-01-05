from django.views.generic import list_detail
from django.contrib.contenttypes.models import ContentType

from publisa import settings as publisa_settings
from publisa.models import Publish

from tagging.models import Tag

def index(request, page=0):
    """ Returns a list of articles """
    return list_detail.object_list(request,
                                   queryset=Publish.objects.published().select_related('content_type'),
                                   page=page,
                                   paginate_by=publisa_settings.PUBLISA_PAGINATE_BY,
                                   template_object_name='publish')

def tag_list(request):
    """ A view displaying the tags for all published items """
    content_types = Publish.objects.published().order_by('content_type').values('content_type').distinct()
    tag_list = set()
    for c in content_types:
        c_type = ContentType.objects.get(pk=c['content_type'])
        model = c_type.model_class()
        tags = Tag.objects.usage_for_queryset(model.publish.all())
        for t in tags: tag_list.add(t)

    print tag_list
