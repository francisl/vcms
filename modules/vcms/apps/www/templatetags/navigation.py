# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
register = template.Library()

@register.inclusion_tag('navigation.html')
def show_product_navigation(navmenu):
    """ return main menu list
        and return the menu currently selected
    """
    navigation_menu = navmenu
    return locals()

