# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template

register = template.Library()

@register.inclusion_tag('tree_dl.html')
def _generetate_dl_tree(data, cssid, cssclass):
    return data, cssid, cssclass

@register.inclusion_tag('tree_li.html')
def _generetate_li_tree(data, cssid, cssclass):
    return data, cssid, cssclass


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
        
