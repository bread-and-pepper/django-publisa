from django.contrib.contenttypes.models import ContentType

import datetime

from publisa.models import Publish
from publisa import settings as lisa_settings

def post_save_handler(sender, instance, created, **kwargs):
    """ Setup the publish item if item is saved """
    publish_type = ContentType.objects.get_for_model(instance)
    try:
        p = Publish.objects.get(content_type__pk=publish_type.id,
                                object_id=instance.id)
    except Publish.DoesNotExist:
        p = None

    # Status is finished, and there is no publish item. So add...
    if instance.status == 2 and not p:
        Publish.objects.create(content_object=instance,
                               publish=datetime.datetime.now(),
                               banner=instance.allow_banners,
                               approved=lisa_settings.PUBLISA_AUTO_PUBLISH)

    # Status is unfinished, yet still it's managed by Publisa. Remove it.
    elif instance.status != 2 and p:
        p.delete()

def post_delete_handler(sender, instance, **kwargs):
    """ Remove the item from Publisa """
    publish_type = ContentType.objects.get_for_model(instance)
    try:
        p = Publish.objects.get(content_type__pk=publish_type.id,
                                object_id=instance.id)
    except Publish.DoesNotExist:
        pass
    else: p.delete()
