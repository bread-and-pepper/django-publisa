from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.timesince import timeuntil, timesince

import datetime

STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Finished')),
)
class PublishManager(models.Manager):
    """ Handle the publishing of items """
    def published(self):
        return self.get_query_set().filter(approved=True,
                                           publish__lte=datetime.datetime.now())

    def get_for_object(self, obj):
        """ Returns the published item for this object. """
        ctype = ContentType.objects.get_for_model(obj)
        try: p = self.get(content_type__pk=ctype.pk,
                          object_id=obj.pk)
        except Publish.DoesNotExist:
            return None
        else: return p

class PublishDescriptor(object):
    """
    A descriptor which provides access to a ``PublishManager`` for
    model classes and simple retrieval, updating and deletion of tags
    for model instances.

    """
    def __get__(self, instance, model):
        if not instance:
            publish_manager = PublishManager()
            publish_manager.model = model
            return publish_manager
        else:
            return Publish.objects.get_for_object(instance)

class Publish(models.Model):
    """
    Publish model which can be inherited into any other model. This way you can
    manage if and when something should get published.

    """
    publish = models.DateTimeField(_('publish'),
                                   default=datetime.datetime.now,
                                   help_text=_('The date of release.'))
    banner = models.BooleanField(_('banner'),
                                 default=True,
                                 help_text=_('Should this item be shown in the banner?'))
    approved = models.BooleanField(_('approved'),
                                   default=False,
                                   editable=False,
                                   help_text=_('Approved by the boss.'))
    objects = PublishManager()

    content_type = models.ForeignKey(ContentType, editable=False, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-publish']
        verbose_name = 'published item'
        verbose_name_plural = 'published items'
        unique_together = ('content_type', 'object_id')

    def __unicode__(self):
        return '%(title)s' % {'title': self.content_object}

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
        if not hasattr(self, 'type_ptr'):
            self.type = ContentType.objects.get_for_model(self.__class__)
        super(Publish, self).save(force_insert, force_update)

    def published_humanised(self):
        """ Show humanised string of the publication date """
        now = datetime.datetime.now()
        if now > self.publish:
            return _('%s ago..') % timesince(self.publish)
        else:
            return _('%s left..') % timeuntil(self.publish)
    published_humanised.short_description = _('Publication')
    published_humanised.allow_tags = True

class Status(models.Model):
    """
    A simple MetaClass which enables the content creator to mark his input as
    draft.

    """
    status = models.IntegerField(_('status'),
                                 choices=STATUS_CHOICES,
                                 default=1,
                                 help_text=_('Draft will not be published.'))

    class Meta:
        abstract = True
