# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.apps.www.models.page import BasicPage as Page
from vcms.apps.www.models.menu import MainMenu
from vcms.apps.www.models.page import Language

register = template.Library()

@register.inclusion_tag('menu/menu_dropdown.html')
def show_dropdown_menu(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    l = Language.objects.get_default()
    try:
        root = MainMenu.objects.get(menu_name=str(l))
    except:
        root = None
    menus = {}
    if root != None:
        for menuitem in root.get_children():
            menus[menuitem] = {}
    
    """
    menus = {}
    for page in Page.objects.get_RootMenu():
        menus[page] = {}
    
    for page in menus:
        menus[page] = Page.objects.get_SubMenu(page)
        
    selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    """
    
    return locals()

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
    print("root = %s" % root)
    
    if root != None:
        main_menu = [ menuitem for menuitem in root.get_children()]
        
    #selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    return locals()

@register.inclusion_tag('submenu.html')
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