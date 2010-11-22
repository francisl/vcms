# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.www.models.containers import ContainerWidgets
from vcms.simpleblogs.views import get_side_menu
register = template.Library()

@register.inclusion_tag('newsblogs_navigation.html')
def newsblogs_navigation(current_page):
    categories, archives, older_archives = get_side_menu(current_page)
    return {'categories': categories
            ,'archives': archives
            ,'older_archives': older_archives
            ,'page': current_page
            }
