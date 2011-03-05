# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

def page_info(request):
    if hasattr(request, 'current_page'):
        return { 'page_info' : request.current_page }
    return {}

def cms_menu(request):
    to_return = {}
    if hasattr(request, 'cms_selected_menu'):
        to_return.update(cms_selected_menu = request.cms_selected_menu)
    if hasattr(request, 'cms_menu'):
        print("context processoring cms_menu")
        to_return.update(cms_menu = request.cms_menu)
    if hasattr(request, 'cms_submenu'):
        to_return.update(cms_submenu = request.cms_submenu)
    if hasattr(request, 'cms_basepath'):
        to_return.update(cms_basepath = request.cms_basepath)
        
    return to_return

def cms_menu_extrapath(request):
    if hasattr(request, 'cms_menu_extrapath'):
        return { 'cms_menu_extrapath' : request.cms_menu_extrapath }
