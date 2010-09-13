# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('cms_theme.html')
def get_selected_theme():
    return {'theme' : settings.SELECTED_THEME }
 