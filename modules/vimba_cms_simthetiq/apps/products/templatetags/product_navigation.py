# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
from vimba_cms_simthetiq.apps.products.models import Category Product

register = template.Library()

@register.inclusion_tag('menu/menu_dropdown.html')
def show_product_navigation(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    
    categories = {}  
    
    
    
    menus = {}
    for page in Page.objects.get_RootMenu():
        menus[page] = {}
    
    for page in menus:
        menus[page] = Page.objects.get_SubMenu(page)
        
    selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    return locals()

