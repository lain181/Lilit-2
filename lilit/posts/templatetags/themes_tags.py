from django import template

from posts.models import Themes

register = template.Library()

@register.simple_tag
def get_themes():
    return Themes.objects.all().only('theme', 'slug')