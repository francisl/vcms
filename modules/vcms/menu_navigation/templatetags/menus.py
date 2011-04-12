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

def is_menu_selected(menu, current_menu):
    if menu == current_menu:
        return True
    return False

@register.inclusion_tag('menu/menu_dropdown.html')
def show_dropdown_menu(current_menu=None):
    """ return main menu list
        and return the menu currently selected
    """
    menus = []
    for menuitem in CMSMenu.objects.get_roots(language='en'):
        #selected=is_menu_selected(menuitem, current_page.get_menu.get_root().id)
        menu = dict(menu=menuitem
                    ,selected=is_menu_selected(menuitem, current_menu)
                    ,submenus=[])
        for submenu in CMSMenu.objects.get_displayable_children(menuitem):
            is_selected = is_menu_selected(submenu, current_menu)
            submenudict = dict(menu=submenu, selected=is_selected, submenu=[])
            menu['submenus'].append(submenudict)
            if is_selected:
                menu['selected'] = True
        menus.append(menu)
    return locals()
    

@register.inclusion_tag('menu/side_navigation.html')
def show_navigation_menu(current_page=None, cms_basepath=None, cms_menu=None, cms_submenu=None, cms_extrapath=None):
    from django.contrib.contenttypes.models import ContentType
    from vcms_simthetiq.simthetiq_dis_navigation.models import MenuNavigation
    ct = ContentType.objects.get(model='menunavigation')
    submenu_for = cms_menu
    if cms_menu.parent:
        submenu_for = cms_menu.parent

    menus =  CMSMenu.objects.get_displayable_children(submenu_for)

    menu_items = []
    for menu in menus :
        menu_info = {}
        menu_info.update(item = menu)
        menu_info.update(selected = True if menu.slug == cms_submenu.slug else False)
        menu_info.update(submenu =  menu.content_object.render_submenu(cms_basepath=cms_basepath ,cms_extrapath = cms_extrapath) if hasattr(menu.content_object, 'render_submenu') else "")
        menu_items.append(menu_info)

    return { 'menu_items' : menu_items, 'cms_menu' : cms_menu }
    
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
