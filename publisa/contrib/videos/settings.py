from django.conf import settings

import os

videola_path = os.path.realpath(os.path.dirname(__file__))

# Destination of the uploaded video's. These shouldn't be public available
# because they will be decoded into flash movies which are public.
VIDEOLA_VIDEO_ROOT = getattr(settings, 'VIDEOLA_VIDEO_ROOT', os.path.join(videola_path, 'videos'))

# The offset in seconds of which a screenshot will be taken to create a
# thumbnail.
VIDEOLA_THUMBNAIL_OFFSET = getattr(settings, 'VIDEOLA_THUMBNAIL_OFFSET', 4)
