# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.apps.www.models import Page

register = template.Library()

@register.inclusion_tag('menu.html')
def show_main_menu(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    main_menu = Page.objects.get_RootMenu()
    selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    return locals()

@register.inclusion_tag('footer_menu.html')
def show_footer_menu(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    main_menu = Page.objects.get_RootMenu()
    selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    return locals()

@register.inclusion_tag('submenu.html')
def show_sub_menu(current_page=None):
    """ return the submenu currently selected
        and the seleted_submenu
    """
    submenu, selected_submenu = Page.objects.get_SubMenu(current_page)
    return locals()
