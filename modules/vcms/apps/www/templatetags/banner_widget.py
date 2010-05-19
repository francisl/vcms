# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.apps.www.models import Banner
import settings
register = template.Library()

# TODO: Make banner more dynamic - Size, page position
@register.inclusion_tag('banner.html')
def show_banner(current_page, MEDIA_URL):
    """ return main menu list
        and return the menu currently selected
    """
    
    #print("STyle. - %s" % style)
    banner, banner_images, has_banner, banner_style = Banner.objects.get_banner(current_page)
    #banner_size = str(banner.width) + str('x') + str(banner.height)
    
    #print("banner_images | %s\nhas_banner | %s\nbanner_style | %s" % (banner, has_banner, banner_style))
    banner_obj = Banner.objects.all()[0]
    #print("banner width | %s\nbanner heigth | %s" % (banner_obj.width, banner_obj.height))
    banner_size = str(banner_obj.width) + str('x') + str(banner_obj.height)
    #print("banner size = %s" % banner_size)
    MEDIA_URL = settings.MEDIA_URL
        
    return locals()

# TODO: Make banner more dynamic - Size, page position
@register.inclusion_tag('banner.html')
def show_banner_generic():
    """ return main menu list
        and return the menu currently selected
    """

    #print("STyle. - %s" % style)
    #try:
    banner_obj = Banner.objects.all()[0]
    banner, banner_images, has_banner, banner_style = banner_obj, banner_obj.get_images(), True, banner_obj.style
    #except:
    #    has_banner = False
    
    MEDIA_URL = settings.MEDIA_URL
    banner_size = str(banner_obj.width) + str('x') + str(banner_obj.height)
    
    return locals()
