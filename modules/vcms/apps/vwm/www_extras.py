# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.apps.www.models import Page

register = template.Library()

@register.inclusion_tag('menu/menu_dropdown.html')
def show_dropdown_menu(current_page=None):
    """ return main menu list
        and return the menu currently selected
    """
    menus = {}
    for page in Page.objects.get_RootMenu():
        menus[page] = {}
    
    for page in menus:
        menus[page] = Page.objects.get_SubMenu(page)
        
    selected_menu = Page.objects.get_RootSelectedMenu(current_page)
    return locals()


@register.inclusion_tag('tree_dl.html')
def _generetate_dl_tree(data, cssid, cssclass):
    return data, cssid, cssclass

@register.inclusion_tag('tree_li.html')
def _generetate_li_tree(data, cssid, cssclass):
    return data, cssid, cssclass

def create_tree_structure(name, items=[], child_selected=False, selected=False, url="#"):
    """ Take required parameters and return a valid dictionary tree node 
    """
    return {"name": name, "items": items, "child_selected":child_selected, "selected":selected, "url":url}

def generate_tree(data, cssid="", cssclass="", type="dl"):
    """ Take a list and generate a html tree
        
        data : a list containing a dictionary
            List item dictionary required field :
            - url : used to generate <a> tag (default="#")
            - name : name used to identified to item (default="Undefined")
            - child_selected : boolean, if one of its childs is selected (default=False)
            - selected : boolean, if the items is selected (default=False)
            - items : list of items (recursive data structure for multi-level tree) (default=[])
        
        cssid : string, id of the list container
        cssclass : string, class name of thelist container
        type : string, either "dl" for a definition list (<dl>/dl>) or "ul" for a unordered list (<ul></ul>)
    
    """
    
    if type == "dl":
        return _generetate_dl_tree(data, cssid, cssclass)
    if type == "li":
        return _generetate_li_tree(data, cssid, cssclass)
        
