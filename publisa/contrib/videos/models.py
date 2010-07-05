from django.db import models
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File

from videola import settings as vid_settings

import commands, os

VIDEO_QUALITY_CHOICES = (
    (1, _('low')),
    (2, _('medium')),
    (3, _('maximum'))
)

class ThumbnailCreationError(Exception):
    """ This exception is thrown when a thumbnail couldn't be created """
    pass

class FlashVideoCreationError(Exception):
    """ This exception is thrown when the flash video couldn't be created """
    pass

storage = FileSystemStorage(location=vid_settings.VIDEOLA_VIDEO_ROOT,
                            base_url='/original')

def upload_to_video(instance, filename):
    ext = filename.split('.')[-1]
    return '%(slug)s.%(ext)s' % {'slug': instance.slug,
                                 'ext': ext}

class VideoSize(models.Model):
    """ Defines the size of a video """
    width = models.PositiveIntegerField(_('width'))
    height = models.PositiveIntegerField(_('height'))

    def __unicode__(self):
        return '%(width)sx%(height)s' % {'width': self.width,
                                         'height': self.height}

class Watermark(models.Model):
    """ Watermarks to overlay on the video """
    title = models.CharField(max_length=255)
    image = models.ImageField(_('image'), upload_to='watermarks/')

    def __unicode__(self):
        return '%s' % self.title

class Video(models.Model):
    """ Model representing a video """
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    quality = models.IntegerField(_('quality'), choices=VIDEO_QUALITY_CHOICES)
    size = models.ForeignKey(VideoSize)
    video = models.FileField(_('video'),
                             upload_to=upload_to_video,
                             storage=storage)
    thumbnail = models.ImageField(_('thumbnail'),
                                  upload_to='videos/',
                                  blank=True,
                                  help_text=_('If left blank this will be auto-generated.'))

    def __unicode__(self):
        return '%s' % self.title

    @property
    def url(self):
        """ Url where the file can be found """
        return '%(media_url)svideos/%(slug)s.flv' % {'media_url': settings.MEDIA_URL,
                                                     'slug': self.slug}

    @property
    def flv_path(self):
        """ Path of flv created file """
        return '%(media_root)svideos/%(slug)s.flv' % {'media_root': settings.MEDIA_ROOT,
                                                      'slug': self.slug}

    @property
    def original_path(self):
        """ Path of uploaded file """
        return '%(root)s%(file)s' % {'root': vid_settings.VIDEOLA_VIDEO_ROOT,
                                     'file': self.video.name}

    @property
    def thumbnail_path(self):
        """ Returns path of thumbnail """
        return '%(video_root)s%(slug)s.png' % {'video_root': vid_settings.VIDEOLA_VIDEO_ROOT,
                                               'slug': self.slug}

    def generate_thumbnail(self):
        """ Generates a thumbnail image to be filled in to the ``thumbnail`` field. """
        thumbnail_cmd = 'ffmpeg -y -i %(source)s -itsoffset -%(thumbnail_offset)s -vcodec png -vframes 1 -an -f rawvideo -s %(size)s %(thumbnail)s' % \
                {'source': self.original_path,
                 'thumbnail_offset': vid_settings.VIDEOLA_THUMBNAIL_OFFSET,
                 'size': self.size,
                 'thumbnail': self.thumbnail_path}
        thumbnail_result = commands.getoutput(thumbnail_cmd)
        # Check if all went right, else raise exception
        if not os.path.isfile(self.thumbnail_path):
            raise ThumbnailCreationError(thumbnail_result)

        # Save the result to the django ``thumbnail`` field.
        f = File(open(self.thumbnail_path))
        filename = 'videos/%(slug)s.png' % {'slug': self.slug}
        self.thumbnail.save(filename, f, save=False)
        self.save(encode=False)
        f.close()
        return True

    def convert_to_flv(self):
        """
        Converts a video to FLV format so it's playable

        @TODO: Raise exceptions when commands go wrong.

        """
        if self.quality == 1:
            quality_settings = '-ab 96k -qscale 4'
        if self.quality == 2:
            quality_settings = '-ab 96k -qscale 2'
        elif self.quality == 3:
            quality_settings = '-qscale .1'

        # Create the FLV.
        ffmpeg_cmd = "ffmpeg -y -i %(source)s -ar 22050 %(quality)s -s %(size)s %(flv)s" % \
                {'source': self.original_path,
                 'quality': quality_settings,
                 'size': self.size,
                 'thumbnail': self.thumbnail_path,
                 'flv': self.flv_path}
        conversion_result = commands.getoutput(ffmpeg_cmd)

        # Check if it all went right, else raise hell!
        if not os.path.isfile(self.flv_path):
            raise FlashVideoCreationError(conversion_result)

        # Add movie information
        flvtool2_result = commands.getoutput('flvtool2 -U %s' % self.flv_path)

    def save(self, encode=True, *args, **kwargs):
        """
        While saving the movie we should also make a .flv file with ffmpeg.

        """
        # First upload the file
        super(Video, self).save(*args, **kwargs)
        if encode:
            self.generate_thumbnail()
            self.convert_to_flv()
