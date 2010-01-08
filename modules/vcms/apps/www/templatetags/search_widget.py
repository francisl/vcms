from django import template

register = template.Library()

@register.inclusion_tag('search_widget.html')
def show_search_box():
    """ search in all pages for query
    """
    return None
