from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django import forms
from django.views.generic import list_detail, date_based
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from artikelly.models import InlineType, Article, Category
from artikelly.forms import get_inline_form
from artikelly.utils import get_model_for_inline
from artikelly import settings as artikelly_settings

def list(request, page=0):
    """ Returns all the published articles """
    return list_detail.object_list(request,
                                   queryset=Article.publish.all(),
                                   template_object_name='article',
                                   page=page,
                                   paginate_by=artikelly_settings.ARTIKELLY_PAGINATE_BY)

def detail(request, slug, year, month, day):
    """ Show the details of an article """
    articles = Article.publish.all()
    return date_based.object_detail(request,
                                    year=year,
                                    month=month,
                                    day=day,
                                    date_field='published_at',
                                    slug=slug,
                                    queryset=articles,)

def archive_day(request, year, month, day):
    """ Return the articles of that day """
    return date_based.archive_day(request,
                                  year=year,
                                  month=month,
                                  day=day,
                                  date_field='published_at',
                                  template_object_name='article',
                                  queryset=Article.publish.all())

def archive_month(request, year, month):
    """ Return the articles posted that month """
    return date_based.archive_month(request,
                                    year=year,
                                    month=month,
                                    date_field='published_at',
                                    template_object_name='article',
                                    queryset=Article.publish.all())

def archive_year(request, year):
    """ Return the articles of that year """
    return date_based.archive_year(request,
                                   year=year,
                                   date_field='published_at',
                                   queryset=Article.publish.all(),
                                   template_object_name='article',
                                   make_object_list=True)


def admin_inline(request, inline_id):
    """ Returns HTML that displays a list of supplied inlines for embedding in the Admin """
    inline_type = get_object_or_404(InlineType,
                                    pk=inline_id)

    app_label, model_name, model = get_model_for_inline(inline_type)

    template = ["admin/%(app_label)s/inline_list_%(model_name)s.html" % {'app_label': app_label,
                                                                         'model_name': model_name},
                "admin/inlines/default_list.html"]

    # Get all objects
    object_list = model.objects.all()

    admin_add = reverse('admin:%(app_label)s_%(model_name)s_add' % {'app_label': app_label,
                                                                    'model_name': model_name})

    context = {'inline': inline_type,
               'object_list': object_list,
               'admin_add': admin_add,
               'model_name': model_name,
               'app_label': app_label }

    return render_to_response(template, context)

def category_list(request):
    """ List of all the categories """
    return list_detail.object_list(request,
                                   queryset=Category.objects.all())

def category_detail(request, slug, page=0):
    """ Details of a category """
    category = get_object_or_404(Category, slug__iexact=slug)

    return list_detail.object_list(request,
                                   queryset=Article.publish.all().filter(category=category),
                                   template_name='artikelly/category_detail.html',
                                   template_object_name='article',
                                   paginate_by=artikelly_settings.ARTIKELLY_PAGINATE_BY,
                                   page=page,
                                   extra_context={'category': category})
