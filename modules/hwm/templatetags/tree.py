# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
register = template.Library()

@register.inclusion_tag('tree/tree_mptt_dl.html')
def generate_dl_tree(data, css_id=None, css_class=None):
    """ TODO: COMPLETE generate_dl_tree templatetags
    """
    print("data = %s" % data.all())
    root = data.all()[0].get_root()
    
    return {"root": root, "cssid":css_id, "cssclass": css_class}

@register.inclusion_tag('tree/tree_li.html')
def generate_li_tree(data, css_id, css_class):
    """ TODO: COMPLETE generate_li_tree templatetags
    """
    return data, css_id, css_class

