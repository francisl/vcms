# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.inclusion_tag('tree_dl.html')
def generetate_dl_tree(data, cssid, cssclass):
    return {"data":data, "cssid":cssid, "cssclass": cssclass}

@register.inclusion_tag('tree_li.html')
def generetate_li_tree(data, cssid, cssclass):
    return data, cssid, cssclass

def _generetate_dl_tree(data, cssid, cssclass):
    """ When called from a function instead of a template tag
    """
    return render_to_string('tree_dl.html', 
                            {"data":data, "cssid":cssid, "cssclass": cssclass}) 

def _generetate_li_tree(data, cssid, cssclass):
    return data, cssid, cssclass

def generate_tree(data, cssid="", cssclass="", type="dl"):
    """ Take a list and generate a html tree
        ˙
        data : a list containing a dictionary
            List item dictionary required field :
            - url : string - used to generate <a> tag (default="#")
            - name : string - name used to identified to item (default="Undefined")
            - child_selected : boolean - if one of its childs is selected (default=False)
            - selected : boolean - if the items is selected (default=False)
            - items : list - list of items (recursive data structure for multi-level tree) (default=[])
        
        id : string id of the list container
        cssclass : string, class name of thelist container
        type : string, either "dl" for a definition list (<dl>/dl>) or "ul" for a unordered list (<ul></ul>)
        
        @example - Without helper:
            >>> from vcms.apps.vwm.tree import generator
            
            # create one item 
            >>> item = {}
            >>> item["name"] = "item_name"
            >>> item["url"] = "/products/"
            >>> item["child_selected"] = False
            >>> item["selected"] = False
            >>> item["items"] = []
            
            #generate the html
            >>> generated_navigation = generator.generate_tree([item,])
            
            #then add the generated code to the navigation section {% block navigation %}
            
        @example - Using the helper:
            >>> from vcms.apps.vwm.tree import generator
            >>> rom vcms.apps.vwm.tree import helper
            
            # create the item
            >>> item = helper.create_tree_node([item_name], url=item.get_absolute_url()))
            
            # generate the html
            >>> generated_navigation = generator.generate_tree([item,])
            
            # then add the generated code to the navigation section {% block navigation %}
            
    """
    
    if type == "dl":
        return _generetate_dl_tree(data, cssid, cssclass)
    if type == "li":
        return _generetate_dl_tree(data, cssid, cssclass)
        # TODO: add generate_li_tree code
        #return _generetate_li_tree(data, cssid, cssclass)
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
