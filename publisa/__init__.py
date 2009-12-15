from publisa.models import PublishDescriptor

class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model for Publisher more than once.
    """
    pass

registry = []
def register(model, banner=True):
    """ Setup a model to be managed by Publisa. """

    if model in registry:
        raise AlreadyRegistered(_('The model %s has already been registered.') % model.__name__)
    registry.append(model)

    # Set the extra attributes
    setattr(model, 'banner', banner)
    setattr(model, 'publish', PublishDescriptor())

    # If the model has no status, always see it as finished
    if not hasattr(model, 'status'):
        setattr(model, 'status', 2)

    # Send a signal to our receivers when the model is updated or deleted.
    from django.db.models import signals
    from publisa.signals import post_save_handler, post_delete_handler

    signals.post_save.connect(post_save_handler, sender=model)
    signals.post_delete.connect(post_delete_handler, sender=model)
