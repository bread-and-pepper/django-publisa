from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
)

class PublishManager(models.Manager):
    """ Handle the publishing of items """
    def published(self):
        return self.get_query_set().filter(status__gte=2,
                                           publish__lte=datetime.datetime.now())

class Publish(models.Model):
    """
    Publish model which can be inherited into any other model. This way you can
    manage if and when something should get published.

    """
    status = models.IntegerField(_('status'),
                                 choices=STATUS_CHOICES,
                                 default=1,
                                 help_text=_('Draft will not be shown on the frontpage.'))
    publish = models.DateTimeField(_('publish'),
                                   default=datetime.datetime.now,
                                   help_text=_('The date it will be published.'))
    banner = models.BooleanField(_('banner'),
                                 default=True,
                                 help_text_('Should this item be shown in the banner?'))
    type = models.ForeignKey(ContentType, editable=False)
    objects = PublishManager()

    class Meta:
        abstract = True
        ordering = ['-publish']

    @property
    def child(self):
        """ Returns the child instance """
        return self.type.get_object_for_this_type(id=self.id)

    @models.permalink
    def get_absolute_url(self):
        """
        The published item doesn't have it's own permalink. It just redirect
        to the permalink of the child model.

        """
        return self.child.get_absolute_url()

    def save(self, force_insert=False, force_update=False):
        """ Custom save method so the child of the published item can be found """
        if not hasattr(self,'type_ptr'):
            self.type = ContentType.objects.get_for_model(self.__class__)
        super(Publish, self).save(force_insert, force_update)
