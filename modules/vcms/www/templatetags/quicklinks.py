# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.www.models import QuickLinks
from django.conf import settings

register = template.Library()


# TODO: Make banner more dynamic - Size, page position
@register.inclusion_tag('quicklinks.html')
def show_quicklinks():
    """ return all the quicklinks
    """
    MEDIA_URL = settings.MEDIA_URL
    quicklinks = QuickLinks.objects.get_quicklinks() 
    return locals()

