from django import template

register = template.Library()

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
                    'publisa/item_publish_list.html',]

                t = template.loader.select_template(templates)
                context = template.Context({'object': obj.content_object,})
                try:
                    rendered = t.render(context)
                except template.TemplateSyntaxError:
                    return ''
                else: return rendered
            else: return ''


