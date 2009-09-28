from django import template
from vimba_cms.apps.www.models import Page

register = template.Library()

@register.inclusion_tag('admin/www/page/page_table.html')
def show_menu_table(lang='en'):
    menu_list = Page.objects.get_RootMenu()
    submenu_list = Page.objects.filter(level=1)

    submenus = {}
    for menu in menu_list:
        submenu  = Page.objects.get_SubMenu(menu)[0]
        submenus[menu.id] = {"menu": menu.id, "submenu": submenu }

    all_pages = Page.objects.get_Published()

    modules = Page.objects.values('module').order_by("module").distinct()
    
    #Generate and dictionnary of page per modules
    # takes all published page on the web site
    # and separate it into modules
    """
    pages ={}
    for page in Page.objects.get_NotDisplay():
        if pages.has_key(page.module):
            pages[page.module].append(page)
        else:
           pages[page.module] = [page ]
    """
    
    return locals()
