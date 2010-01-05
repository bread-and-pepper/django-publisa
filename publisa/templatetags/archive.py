import re

from django import template
from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from tagging.models import TaggedItem

Publish = models.get_model('publisa', 'publish')

register = template.Library()

@register.tag
def get_latest_months(parser, token):
    try:
        tag_name, limit, dummy, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    if dummy != "as":
        raise template.TemplateSyntaxError, "%s mismatch with templatetag" % dummy
    return MonthArchive(limit, var_name)

class MonthArchive(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Publish.objects.published().dates("publish", "month")[:int(self.limit)]
        return ''

@register.tag
def popular_tags(parser, token):
    try:
        tag_name, limit, dummy, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    if dummy != "as":
        raise template.TemplateSyntaxError, "%s mismatch with templatetag" % dummy
    return PopularTags(limit, var_name)

class PopularTags(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name

    def render(self, context):
        tag_list = TaggedItem.objects.annotate(count=Count('tag')).order_by('count')

        context[self.var_name] = tag_list
        return ''

