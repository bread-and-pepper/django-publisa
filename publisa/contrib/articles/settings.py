from django.conf import settings

DEFAULT_CLASSES = (('centerpiece', 'centerpiece'),
                   ('small-left', 'small-left'),
                   ('small-right', 'small-right'))

ARTIKELLY_PAGINATE_BY = getattr(settings, 'ARTIKELLY_PAGINATE_BY', 2)
ARTIKELLY_PHOTO_CLASSES = getattr(settings, 'ARTIKELLY_PHOTO_CLASSES', DEFAULT_CLASSES)
