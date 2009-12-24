from django.conf import settings

PUBLISA_PAGINATE_BY = getattr(settings, 'PUBLISA_PAGINATE_BY', 5)
