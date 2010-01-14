from django import template
from django.db import models
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.db import connection

qn = connection.ops.quote_name

def qf(table, field): # quote table and field
    return '%s.%s' % ( qn(table), qn(field) )

def comments_extra_count(queryset):
    """
    Returns a queryset for comments with ``comment_count`` attached.  Comes in
    handy when wanting to sort models on the amount of comments.

    """
    commented_model = queryset.model
    contenttype = ContentType.objects.get_for_model(commented_model)
    commented_table = commented_model._meta.db_table
    comment_table = Comment._meta.db_table

    sql = '''SELECT COUNT(*) FROM %s
             WHERE %s=%%s AND %s=%s
          ''' % (
        qn(comment_table),
        qf(comment_table, 'content_type_id'),
        qf(comment_table, 'object_pk'),
        qf(commented_table, 'id'))

    return queryset.extra(
        select={'comment_count': sql },
        select_params=(contenttype.pk,))

Publish = models.get_model('publisa', 'publish')
register = template.Library()

@register.tag
def most_commented(parsen, token):
    """
    Returns a list of most commented items

    Usage::
        {% most_commented <app>.<model> <total> as <variable> %}

    Example::
        {% most_commented artikelly.article 5 as popular_list %}

    """
    try:
        tag_name, app_model, total, as_name, variable = token.split_contents()
    except:
        raise template.TemplateSyntaxError, '%s is used as "{% most_comment <app>.<model> <total> as <variable> %}' % token.contents.split()[0]

    # Get the corresponding model
    app_label, model = app_model.split('.')
    model = models.get_model(app_label, model)
    if not model:
        raise template.TemplateSyntaxError, '%s could not be found.' % app_model

    # Check if the model has comments
    if not hasattr(model, 'comments'):
        raise template.TemplateSyntaxError, 'Could not find comments for %s!' % app_model

    # Check if total is an integer
    try:
        total = int(total)
    except ValueError:
        raise template.TemplateSyntaxError, '"%s" should be an integer' % total

    # Fourth argument should be 'as'
    if not as_name == 'as': raise template.TemplateSyntaxError, 'Fourth argument should be "as" not "%s"!' % as_name

    return MostCommented(model, total, variable)

class MostCommented(template.Node):
    def __init__(self, model, total, var):
        self.model = model
        self.total = total
        self.var = var

    def render(self, context):
        object_list = self.model.objects.all()
        commented_list = comments_extra_count(object_list).order_by('-comment_count')[self.total]

        context[self.var] = commented_list
        return ''

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
        publish_list = Publish.objects.published().filter(banner=True).select_related('content_type')[:self.total]
        banner_list = []
        for p in publish_list:
            # Only add banners which have an image
            if p.get_banner_image():
                d = {'app': p.content_type.app_label,
                     'model': p.content_type.name}

                templates = [
                    '%(app)s/%(model)s_publish_banner.html' % d,
                    'publisa/%(model)s_publish_banner.html' % d,
                    'publisa/item_publish_banner.html',]
                t = template.loader.select_template(templates)
                banner_context = template.Context({'object': p.content_object,
                                                   'publish': p})
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

    return RenderTemplates(obj, 'publish_list')

@register.tag
def render_admin_preview(parser, token):
    """
    Displays the published item as a preview in the admin

    Usage::
        {% render_admin_preview object %}

    """
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%s requires arguments' % token.contents.split()[0]

    return RenderTemplates(obj, 'publish_admin')

class RenderTemplates(template.Node):
    """ Renders the supplied objects """
    def __init__(self, object, template_prefix):
        self.object = template.Variable(object)
        self.template_prefix = template_prefix

    def render(self, context):
        try:
            obj = self.object.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        else:
            if hasattr(obj, 'publish'):
                d = {'app': obj.content_type.app_label,
                     'model': obj.content_type.name,
                     'prefix': self.template_prefix}

                templates = [
                    '%(app)s/%(model)s_%(prefix)s.html' % d,
                    'publisa/%(model)s_%(prefix)s.html' % d,
                    'publisa/item_%(prefix)s.html' % d,]

                t = template.loader.select_template(templates)
                context = template.Context({'publish': obj,
                                            'object': obj.content_object,})
                try:
                    rendered = t.render(context)
                except template.TemplateSyntaxError:
                    return ''
                else: return mark_safe(rendered)
            else: return ''
