from django.contrib import admin
from django.http import HttpResponse
from videola.models import Video, VideoSize, Watermark
from videola.utils import ProgressUploadHandler

class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js', 'videola/js/videola.js')

admin.site.register(Video, VideoAdmin)
admin.site.register(VideoSize)
