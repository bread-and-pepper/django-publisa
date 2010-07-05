
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from tagging.fields import TagField

from artikelly.render import inlines

import publisa

def upload_to_photo(instance, filename):
    """ Upload a single photo to a date based directory. Filename is a slug. """
    ext = filename.split('.')[-1]
    return 'photos/%(slug)s.%(ext)s' % \
            {'slug': instance.slug,
             'ext': ext,}

class Category(models.Model):
    """ Category model. """
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('artikelly-category-detail', None, {'slug': self.slug})

class Article(publisa.models.Status):
    title = models.CharField(_('title'),
                             max_length=124)
    slug = models.SlugField(_('slug'),
                            help_text=_('Used to create the URL for this article.'))
    author = models.ForeignKey(User,
                               verbose_name=_('Author'))
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    teaser = models.TextField(_('teaser'),
                              blank=True,
                              help_text=_('If left blank, the entire post will \
                                          be shown on the frontpage.'))
    body = models.TextField(_('body'))
    tags = TagField(_('tags'), help_text=_('Add tags so the article can be categorised.'))
    allow_comments = models.BooleanField(_('allow comments'),
                                         default=True,)
    created = models.DateTimeField(_('created'),
                                   auto_now_add=True)
    modified = models.DateTimeField(_('modified'),
                                    auto_now=True)

    # Automaticly updated, not editable
    teaser_html = models.TextField(_('teaser html'), blank=True)
    body_html = models.TextField(_('body html'), blank=True)

    # Optional for publisa
    published_at = models.DateTimeField(_('published at'), blank=True, null=True, editable=False)

    # Comments
    comments = generic.GenericRelation(Comment, content_type_field='content_type', object_id_field='object_pk')

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    @models.permalink
    def get_absolute_url(self):
        return ('artikelly-detail', (), {
            'year': self.published_at.year,
            'month': self.published_at.strftime('%b').lower(),
            'day': self.published_at.day,
            'slug': self.slug })

    def __unicode__(self):
        return '%(title)s' % {'title': self.title}

    def save(self, force_insert=False, force_update=False):
        """ Override the save method to parse the markdown in HTML """
        self.teaser_html = inlines(self.teaser)
        self.body_html = inlines(self.body)
        super(Article, self).save(force_insert, force_update)

    @property
    def publish_rss_title(self):
        return '%(title)s'% {'title': self.title }

    @property
    def publish_rss_description(self):
        return '%(description)s'% {'description': self.teaser_or_body }

    @property
    def publish_banner_image(self):
        """
        This method get's utilised by Publisa to get the banner image.

        In artikelly we have chosen to look for photo inlines and return the
        first found photo as a banner image.

        """
        inline_list = inlines(self.teaser, return_list=True)
        inline_list += inlines(self.body, return_list=True)
        if inline_list:
            for item in inline_list:
                if item.__class__.__name__ == 'Photo':
                    return item.photo
            return None
        else: return None

    @property
    def teaser_or_body(self):
        """ If the teaser is not filled in, than return the body """
        if not self.teaser:
            return self.body_html
        else: return self.teaser_html

class InlineType(models.Model):
    """ InlineType model """
    title = models.CharField(max_length=200)
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content type'))

    class Meta:
        verbose_name = 'inline'
        verbose_name_plural = 'inlines'

    def __unicode__(self):
        return self.title

class Photo(models.Model):
    """ An article can have multiple photo's """
    photo = models.ImageField(_('photo'), upload_to=upload_to_photo)
    title = models.CharField(_('title'),
                             max_length=256,
                             help_text=_('This will be shown when people hover above the photo.'))
    date_added = models.DateTimeField(_('date added'),
                                      auto_now_add=True)

    def __unicode__(self):
        return '%(title)s' % {'title': self.title }

    @property
    def slug(self):
        return slugify(self.title)

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photo\'s')
        ordering = ['-date_added']

publisa.register(Article, allow_banners=True, admin_preview=True)
