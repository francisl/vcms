from django import template

register = template.Library()

@register.inclusion_tag('search_plugin.html')
def show_search_box():
    """ search in all pages for query
    """
    return None
