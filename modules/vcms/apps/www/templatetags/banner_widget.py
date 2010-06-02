# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.apps.www.models import Banner
import settings
register = template.Library()


def print_log(banner, has_banner):
    print("banner | %s" % banner)
    print("banner_images | %s" % banner.get_images())
    print("has_banner | %s" % has_banner) 
    print("banner_style | %s" % banner.style)
    
    
# TODO: Make banner more dynamic - Size, page position
@register.inclusion_tag('banner.html')
def show_banner(current_page=None, MEDIA_URL=''):
    """ return main menu list
        and return the menu currently selected
    """
    #print("current page = %s" % current_page)
    banner, banner_images, has_banner = Banner.objects.get_banner(current_page)
    #print_log(banner, has_banner)
    return locals()

# TODO: Make banner more dynamic - Size, page position
@register.inclusion_tag('banner.html')
def show_banner_generic():
    """ return main menu list
        and return the menu currently selected
    """
    try:
        banner, banner_images, has_banner = Banner.objects.get_banner(None)
        banner_size = banner.get_size()
    except:
        has_banner = False
    
    MEDIA_URL = settings.MEDIA_URL
   
    return locals()
