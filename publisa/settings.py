from django.conf import settings

PUBLISA_PAGINATE_BY = getattr(settings, 'PUBLISA_PAGINATE_BY', 10)

PUBLISA_AUTO_PUBLISH = getattr(settings, 'PUBLISA_AUTO_PUBLISH', False)
