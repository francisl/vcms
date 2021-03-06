# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.template.loader import render_to_string

def _generate_dl_tree(data, css_id, css_class):
    """ When called from a function instead of a template tag
    """
    return render_to_string('tree/tree_dl.html', 
                            {"data":data, "css_id":css_id, "css_class": css_class}) 

def _generate_li_tree(data, css_id, css_class):
    return data, css_id, css_class

def generate_tree(data, navigation_title=None, css_id="", css_class="", type="dl"):
    """ Take a list and generate a html tree
        @param data: a list containing a dictionary
            List item dictionary required field :
            @key url : string - used to generate <a> tag (default="#")
            @key name : string - name used to identified to item (default="Undefined")
            @key child_selected : boolean - if one of its childs is selected (default=False)
            @key selected : boolean - if the items is selected (default=False)
            @key items : list - list of items (recursive data structure for multi-level tree) (default=[])
            @key category : string - the category where the item belongs, like fruit for apple
        
        @param naviagtion_title: string - Put this as the header of the tree
        @param css_id: string id of the list container
        @param css_class: string, class name of thelist container
        @param type: string, either "dl" for a definition list (<dl>/dl>) or "ul" for a unordered list (<ul></ul>)
    """
    
    if type == "dl":
        return _generate_dl_tree(data, css_id, css_class)
    if type == "li":
        return _generate_dl_tree(data, css_id, css_class)
        # TODO: add generate_li_tree code
        #return _generate_li_tree(data, css_id, css_class)
        