from django.conf import settings

# How much pagination should there be on the frontpage
PUBLISA_PAGINATE_BY = getattr(settings, 'PUBLISA_PAGINATE_BY', 10)

# Don't go to the publish screen first but automaticly publish the items.
PUBLISA_AUTO_PUBLISH = getattr(settings, 'PUBLISA_AUTO_PUBLISH', False)

# Which keys in the cache should be reset.
PUBLISA_CACHE_CLEAR_KEYS = getattr(settings, 'PUBLISA_CACHE_CLEAR_KEYS', ())
