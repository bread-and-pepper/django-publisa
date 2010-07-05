from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.conf import settings
from django.template import TemplateSyntaxError

from markdown import markdown
import re

inline_re = r'@\[inline type=(?P<app_label>\w+).(?P<model_name>\w+) id=(?P<id>\d+) class=(?P<class>[-\w]+)\]'

def get_inline(app_label, model_name, id):
    """ Returns the object where the inline references to """
    # Lookup content-type
    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model = content_type.model_class()
    except ContentType.DoesNotExist:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Inline ContentType not found."
    # Get the object
    try:
        obj = model.objects.get(pk=id)
    except model.DoesNotExist:
        raise model.DoesNotExist, "%s with pk of '%s' does not exist" % (model_name, id)
    return obj

def render_inline(match):
    """ Returns the HTML for this inline """
    app_label = match.group('app_label')
    model_name = match.group('model_name')
    id = match.group('id')
    inline_class = match.group('class')

    try:
        inline = get_inline(app_label, model_name, id)
    except:
        return ''
    else:
        context = {'content_type':"%s.%s" % (app_label, model_name),
                   'object': inline,
                   'class': inline_class,
                   'media_url': settings.MEDIA_URL}

        templates = ["inlines/%s_%s.html" % (app_label, model_name),
                     "inlines/default.html"]
        return render_to_string(templates, context)

def inlines(text, return_list=False, **kwargs):
    """
    Parses all the inlines in a text

    Can either return a list of all the inline items, or substitute the inline
    syntax with the the the content supllied in their templates.

    """
    if not return_list:
        markdowned = markdown(text, **kwargs)
        return re.sub(inline_re, render_inline, markdowned)
    else:
        inline_list = []
        for match in re.finditer(inline_re, text):
            app_label = match.group('app_label')
            model_name = match.group('model_name')
            id = match.group('id')
            inline_class = match.group('class')

            inline_list.append(get_inline(app_label, model_name, id))
        return inline_list
