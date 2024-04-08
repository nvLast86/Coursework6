from django import template
from config import settings

register = template.Library()

@register.simple_tag()
def mediapath(image_name):
    return f'{settings.MEDIA_URL}{image_name}'
