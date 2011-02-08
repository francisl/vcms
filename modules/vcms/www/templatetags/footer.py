__author__ = 'arsavard'
from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('footer.html')
def show_footer():
    """ return the footer defined in the admin """
    page_info = {}
    page_info.update(data = { 'title': settings.SITE_NAME
                                ,'description':settings.SITE_DESCRIPTION
                                ,'footer':settings.FOOTER_HTML })
    return locals()
