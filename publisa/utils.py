from publisa.models import Publish

def is_published(object):
    """ Checks if an object is published, if so return True, else False. """
    ctype = Contentype.objects.get_for_model(obj)
    try:
        object = Publish.get(content_type=ctype,
                             object_id=object.id)
    except Publish.DoesNotExist:
        return False
    else: return True
