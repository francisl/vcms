# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from django.template.loader import render_to_string

from vcms.www.models.page import BasicPage as Page
from vcms.www.models.menu import CMSMenu
from site_language.models import Language

from hwm.tree import helper
from hwm.tree import generator

register = template.Library()

@register.inclusion_tag('menu/menu_dropdown.html')
def show_dropdown_menu(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    menus = []
    for menuitem in CMSMenu.objects.get_roots(language='en'):
        menu = dict(menu=menuitem, submenus=[])
        for submenu in CMSMenu.objects.get_displayable_children(menuitem):
            submenudict = dict(menu=submenu, submenu=[])
            menu['submenus'].append(submenudict)
        menus.append(menu)
    return locals()
    

@register.inclusion_tag('menu/side_navigation.html')
def show_navigation_menu(current_page=None):
    return show_dropdown_menu()
    
@register.inclusion_tag('menu/menu.html')
def show_main_menu(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    l = Language.objects.get_default()
    try:
        root = MainMenu.objects.get(menu_name=str(l), depth=0)
    except:
        root = None
    
    if root != None:
        main_menu = [ menuitem for menuitem in root.get_children()]
        
    #selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    return locals()

@register.inclusion_tag('menu/submenu.html')
def show_sub_menu(current_page=None):
    """ return the submenu currently selected
        and the seleted_submenu
    """
    submenu, selected_submenu = Page.objects.get_SubMenu(current_page)
    return locals()


@register.inclusion_tag('menu/footer_menu.html')
def show_footer_menu(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    main_menu = Page.objects.get_RootMenu()
    selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    return locals()
