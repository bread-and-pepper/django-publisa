from columnadia.models import Columnist, Column

from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page

import datetime

def index(request, page=None):
    """ Returns all the columns """
    return list_detail.object_list(request,
                                   queryset=Column.publish.all(),
                                   page=page,)

def columnist_detail(request, columnist, redirect_last=False):
    """
    Returns all columns from a columnist or if ``redirect_last`` is enabled
    will redirect to the last column of this columnist.

    """
    columnist = get_object_or_404(Columnist, slug__iexact=columnist)
    if redirect_last:
        # Get the last column.
        try:
            column = Column.objects.filter(columnist=columnist)[0]
        except IndexError:
            pass
        else:
            return redirect(column)

    return direct_to_template(request,
                              template='columnadia/columnist_detail.html',
                              extra_context={'columnist': columnist})

def column_detail(request, columnist, column):
    """ Returns a column from a columnist """
    columns = Column.publish.all().filter(columnist__slug=columnist)

    # Columns without the current column
    columns_ex = columns.exclude(slug__iexact=column)
    return list_detail.object_detail(request,
                                     queryset=columns,
                                     slug=column,
                                     extra_context={'column_list': columns,
                                                    'column_list_ex': columns_ex})
