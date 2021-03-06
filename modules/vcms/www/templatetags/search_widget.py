from django import template

register = template.Library()

@register.inclusion_tag('search/search_widget.html')
def show_search_box():
    """ search in all pages for query
    """
    return None

@register.inclusion_tag('search/detailed_search_widget.html')
def show_detailed_search_box():
    """ search in all pages for query
    """
    return None
