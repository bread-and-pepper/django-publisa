from django import template
from django.template.loader import render_to_string
from django.conf import settings

# Flowplayer
# http://flowplayer.org/
register = template.Library()
@register.tag
def flowplayer(parser, token):
    """ Returns the HTML for an embedded video """
    try:
        tag_name, video = token.split_contents()
    except:
        raise template.TemplateSyntaxError, '%s is used as "{% flowplayer <video> %}".'

    return EmbedPlayer(video, 'flowplayer')


@register.inclusion_tag('videola/flowplayer_js.html')
def flowplayer_js():
    return {'flowplayer_js': '%svideola/flowplayer/flowplayer-3.1.4.min.js' % settings.MEDIA_URL}

# JW Player
# http://www.longtailvideo.com/players/

@register.tag
def jwplayer(parser, token):
    """ Returns the HTML for an embedded video """
    try:
        tag_name, video = token.split_contents()
    except:
        raise template.TemplateSyntaxError, '%s is used as "{% flowplayer <video> %}".'
    return EmbedPlayer(video, 'jwplayer')

# Generic embedder
class EmbedPlayer(template.Node):
    def __init__(self, video, player):
        self.video = template.Variable(video)
        self.player = player

    def render(self, context):
        try:
            video = self.video.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        else:
            return render_to_string('videola/%s_embed.html' % self.player,
                                    {'video': video,
                                     'media_url': settings.MEDIA_URL})
