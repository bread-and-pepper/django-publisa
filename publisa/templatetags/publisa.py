from django import template
from django.db import models
from django.utils.safestring import mark_safe

Publish = models.get_model('publisa', 'publish')

register = template.Library()

@register.tag
def render_banners(parser, token):
    """
    Returns a list of rendered banners for published items

    Usage::
        {% render_banners <amount> as <variable> %}

    Example::
        {% render_banners 5 as banner_list %}

    """
    try:
        tag_name, total, dummy, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%s is used as "{% render_banners <amount> as <variable> %}".' % token.contents.split()[0]

    try:
        total = int(total)
    except ValueError:
        raise template.TemplateSyntaxError, 'the amount must me an integer, not %s' % total

    if dummy != 'as': raise templateTemplateSyntaxError, 'third argument must be as'
    return RenderBanners(total, var_name)

class RenderBanners(template.Node):
    def __init__(self, total, var_name):
        self.total = total
        self.var_name = var_name

    def render(self, context):
        # get latest x amount of published items
        publish_list = Publish.objects.published().select_related('content_type')[:self.total]
        banner_list = []
        for p in publish_list:
            d = {'app': p.content_type.app_label,
                 'model': p.content_type.name}

            templates = [
                '%(app)s/%(model)s_publish_banner.html' % d,
                'publisa/%(model)s_publish_banner.html' % d,
                'publisa/item_publish_banner.html',]
            t = template.loader.select_template(templates)
            banner_context = template.Context({'object': p.content_object,})
            banner_list.append(mark_safe(t.render(banner_context)))
        context[self.var_name] = banner_list
        return ''

@register.tag
def render_published(parser, token):
    """
    Displays the published item by searching for a ``publish_list`` template.

    Usage::
        {% render_published object %}

    """
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%s requires arguments' % token.contents.split()[0]

    return RenderPublished(obj)

class RenderPublished(template.Node):
    def __init__(self, object):
        self.object = template.Variable(object)

    def render(self, context):
        try:
            obj = self.object.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        else:
            if hasattr(obj, 'publish'):
                d = {'app': obj.content_type.app_label,
                     'model': obj.content_type.name}

                templates = [
                    '%(app)s/%(model)s_publish_list.html' % d,
                    'publisa/%(model)s_publish_list.html' % d,
                    'publisa/item_publish_list.html',]

                t = template.loader.select_template(templates)
                context = template.Context({'object': obj.content_object,})
                try:
                    rendered = t.render(context)
                except template.TemplateSyntaxError:
                    return ''
                else: return rendered
            else: return ''


