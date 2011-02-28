# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

def page_info(request):
    if hasattr(request, 'current_page'):
        return { 'page_info' : request.current_page }
    return {}

def cms_menu(request):
    if hasattr(request, 'cms_selected_menu'):
        return { 'cms_selected_menu' : request.cms_selected_menu }
    return {}
