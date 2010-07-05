from django.db.models import get_model

def get_model_for_inline(inline_type):
    """ Returns the ``app_label`` and ``model_name`` for inline_type. """
    app_label = inline_type.content_type.app_label
    model_name = inline_type.content_type.model
    model = get_model(app_label, model_name)

    return app_label, model_name, model
