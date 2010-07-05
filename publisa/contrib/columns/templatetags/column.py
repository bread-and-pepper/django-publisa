from django.db import models
from django import template

import re

register = template.Library()
Columnist = models.get_model('columnadia', 'columnist')
Column = models.get_model('columnadia', 'column')


@register.tag
def get_columns(parser, token):
    """
    Gets all the columns and stores them in a variable

    Syntax::

        {% get_columns [limit] as [var_name] %}

    Example usage::

        {% get_columns 10 as columnists %}

    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    limit, var_name = m.groups()
    return GetColumns(limit, var_name)

class GetColumns(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Column.publish.all().order_by('-published_at')[:int(self.limit)]
        return ''

@register.tag
def get_columnists(parser, token):
    """
    Gets all the columnists and stores them in a variable

    Syntax::

        {% get_columnists [limit] as [var_name] %}

    Example usage::

        {% get_columnists 10 as columnists %}

    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return GetColumnists(format_string, var_name)

class GetColumnists(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Columnist.objects.all()[:int(self.limit)]
        return ''

