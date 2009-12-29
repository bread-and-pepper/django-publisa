from django import template
from django.template import RequestContext
from django.utils.safestring import mark_safe

register = template.Library()

@register.tag
def render_pagination(parser, token):
    """
    Returns a pagination template. Does require you to set the enable
    ``django.core.context_processors.request`` inside the
    ``TEMPLATE_CONTEXT_PROCESSORS``.

    Usage::
        {% render_pagination <adjacent pages> <template name> %}

    Example::
        {% render_pagination 5 'artikelly/pagination.html' %}

    """
    try:
        tag_name, adjacent_pages, template_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%s is used as "{% render_pagination <adjacent pages> <template name> %}".' % token.contents.split()[0]

    try:
        adjacent_pages = int(adjacent_pages)
    except ValueError:
        raise template.TemplateSyntaxError, 'second argument must be an integer'

    return RenderPagination(adjacent_pages, template_name)

class RenderPagination(template.Node):
    def __init__(self, adjacent_pages, template_name):
        self.adjacent_pages = adjacent_pages
        self.template_name = template_name

    def render(self, context):
        templates = [
            '%s' % self.template_name,
            'publisa/paginator.html',]

        t = template.loader.select_template(templates)

        startPage = max(context['page'] - self.adjacent_pages, 1)
        if startPage <= 3:
            startPage = 1

        endPage = context['page'] + self.adjacent_pages + 1
        if endPage >= context['pages'] - 1:
            endPage = context['pages'] + 1

        page_numbers = [n for n in range(startPage, endPage)
                        if n > 0 and n <= context['pages']]

        page_obj = context['page_obj']
        paginator = context['paginator']

        c = RequestContext(context['request'],
                           {'page_obj': page_obj,
                            'paginator': paginator,
                            'hits': context['hits'],
                            'results_per_page': context['results_per_page'],
                            'page': context['page'],
                            'pages': context['pages'],
                            'page_numbers': page_numbers,
                            'next': context['next'],
                            'previous': context['previous'],
                            'has_next': context['has_next'],
                            'has_previous': context['has_previous'],
                            'show_first': 1 not in page_numbers,
                            'show_last': context['pages'] not in page_numbers,})
        return t.render(c)
