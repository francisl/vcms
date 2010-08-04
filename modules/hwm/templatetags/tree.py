# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
register = template.Library()

@register.inclusion_tag('tree/tree_mptt_dl.html')
def generate_dl_tree(data, css_id=None, css_class=None):
    """ TODO: COMPLETE generate_dl_tree templatetags
    """
    try:
        root = data.all()[0].get_root()
    except:
        root = []
        
    if data.all():
        current_node = data.all()[0]
    else:
        current_node = None 
    
    
    return {"root": root, "current_menu": current_node, "cssid":css_id, "cssclass": css_class}

@register.inclusion_tag('tree/tree_li.html')
def generate_li_tree(data, css_id, css_class):
    """ TODO: COMPLETE generate_li_tree templatetags
    """
    return data, css_id, css_class

