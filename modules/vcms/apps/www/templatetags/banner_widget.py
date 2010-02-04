# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.apps.www.models import Banner

register = template.Library()

# TODO: Make banner more dynamic - Size, page position
@register.inclusion_tag('banner.html')
def show_banner(current_page, MEDIA_URL):
    """ return main menu list
        and return the menu currently selected
    """
    
    #print("STyle. - %s" % style)
    banner, banner_images, has_banner, banner_style = Banner.objects.get_banner(current_page)
    
    print("banner_images | %s\nhas_banner | %s\nbanner_style | %s" % (banner, has_banner, banner_style))
    return locals()
