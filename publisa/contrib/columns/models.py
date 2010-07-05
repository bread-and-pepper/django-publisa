from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from tagging.fields import TagField

import publisa, markdown

def upload_to_headshot(instance, filename):
    """ Upload a single photo to a date based directory. Filename is a slug. """
    ext = filename.split('.')[-1]
    return 'columnists/%(name)s.%(ext)s' % \
            {'name': slugify(instance.user.get_full_name()),
             'ext': ext,}

class Columnist(models.Model):
    """ The writer of columns """
    user = models.ForeignKey(User, verbose_name=_('user'))
    headshot = models.ImageField(_('headshot'), upload_to=upload_to_headshot)
    annotation = models.CharField(_('annotation'), max_length=256, help_text=_('Short text about tho columnist.'))
    biography = models.TextField(_('biography'))
    slug = models.SlugField(_('slug'), blank=True, unique=True)

    @models.permalink
    def get_absolute_url(self):
        return ('columnadia-columnist-detail', (), {'columnist': self.slug})

    def __unicode__(self):
        return '%s' % self.user.get_full_name()

    class Meta:
        verbose_name = _('columnist')
        verbose_name_plural = _('columnists')
        ordering = ['-user__last_name']

class Column(models.Model):
    """ A piece of text """
    columnist = models.ForeignKey(Columnist, verbose_name=_('columnist'), related_name='columns')
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    teaser = models.TextField(_('teaser'),
                              blank=True,
                              help_text=_('Leave this blank if it\'s a short column. Than the entire column will be displayed on the frontpage.'))
    body = models.TextField(_('body'))
    tags = TagField(_('tags'))

    # Fields to be rendered
    teaser_html = models.TextField(_('html teaser'), blank=True, editable=False)
    body_html = models.TextField(_('html body'), blank=True, editable=False)

    # Extra optional field for Publisa
    published_at = models.DateTimeField(_('published at'), blank=True, null=True, editable=False)

    # Comments
    comments = generic.GenericRelation(Comment, content_type_field='content_type', object_id_field='object_pk')

    class Meta:
        verbose_name = ('column')
        verbose_name_plural = ('columns')
        ordering = ('-published_at', 'title')

    def __unicode__(self):
        return _('%(columnist)s: %(title)s') % {'title': self.title,
                                                'columnist': self.columnist.user.get_full_name()}

    @models.permalink
    def get_absolute_url(self):
        return ('columnadia-column-detail', (), {'columnist': self.columnist.slug,
                                                 'column': self.slug})

    def publish_banner_image(self):
        return self.columnist.headshot

    @property
    def publish_rss_title(self):
        return '%(author)s: %(title)s' % {'author': self.columnist,
                                          'title': self.title }

    @property
    def publish_rss_description(self):
        return '%(description)s' % {'description': self.teaser_or_body }

    @property
    def teaser_or_body(self):
        """ If the teaser is not filled in, than return the body """
        if not self.teaser:
            return self.body_html
        else: return self.teaser_html

    def save(self, force_insert=False, force_update=False):
        """ Overwrite the save model so the HTML parts get filled in """
        self.teaser_html = markdown.markdown(self.teaser)
        self.body_html = markdown.markdown(self.body)
        super(Column, self).save(force_insert=force_insert, force_update=force_update)

publisa.register(Column, allow_banners=True, admin_preview=True)
