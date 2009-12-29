from django.utils.translation import ugettext as _

from publisa.models import PublishDescriptor

registry = []
def register(model, allow_banners=False, admin_preview=False):
    """
    Setup a model to be managed by Publisa.

    """
    if model not in registry:
        print "SETTING ADMIN %s for %s" % (admin_preview, model)
        print "SETTING BANNERS %s for %s" % (allow_banners, model)

        # Set the extra attributes
        setattr(model, 'allow_banners', allow_banners)
        setattr(model, 'admin_preview', admin_preview)
        setattr(model, 'publish', PublishDescriptor())

        # If the model has no status, always see it as finished
        if not hasattr(model, 'status'):
            setattr(model, 'status', 2)

        # Send a signal to our receivers when the model is updated or deleted.
        from django.db.models import signals
        from publisa.signals import post_save_handler, post_delete_handler

        signals.post_save.connect(post_save_handler, sender=model)
        signals.post_delete.connect(post_delete_handler, sender=model)

    registry.append(model)
