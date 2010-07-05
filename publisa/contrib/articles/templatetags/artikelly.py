from django import template
from django.db import models

import re

Category = models.get_model('artikelly', 'category')

register = template.Library()

class ArticleCategories(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        categories = Category.objects.all()
        context[self.var_name] = categories
        return ''

@register.tag
def get_article_categories(parser, token):
    """
    Gets all article categories.
    
    Syntax::

        {% get_article_categories as [var_name] %}

    Example usage::

        {% get_article_categories as category_list %}

    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return ArticleCategories(var_name)
