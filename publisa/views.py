from django.views.generic import list_detail
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from publisa import settings as publisa_settings
from publisa.models import Publish

from tagging.models import Tag, TaggedItem

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

    return direct_to_template(request,
                              'publisa/tag_list.html',
                              extra_context={'object_list': tag_list})

def tag_detail(request, slug):
    """ Returns all the published items with this tag """
    tag_name = slug.replace('-', ' ')
    tag = get_object_or_404(Tag, name__iexact=slug)

    extra_context = {'tag': tag}
    # Get distinct content types that are published
    content_types = Publish.objects.published().order_by('content_type').values('content_type').distinct()

    for c in content_types:
        c_type = ContentType.objects.get(pk=c['content_type'])
        model = c_type.model_class()
        verbose_name = model._meta.verbose_name

        # Get all published items for this content type
        object_list = TaggedItem.objects.get_by_model(model.publish.all(), tag)

        # Add those items to the extra context
        extra_context['%(verbose)s_list' % {'verbose': verbose_name}] = object_list

    return direct_to_template(request,
                              'publisa/tag_detail.html',
                              extra_context=extra_context)
