# encoding: utf-8
# copyright Vimba inc. 2011
# programmer : Francis Lavoie

import re

from vcms.www.models.menu import CMSMenu

def _get_page_parameters(page=None):
    """ Set the default parameter for a CMS page """
    page_info = { 'module' : None, 'current_page' : page }
    page_info.update(menu_style = CMSMenu.DROPDOWN_MENU)
    
    if page:
        page_info.update(module = page.__dict__.get('module'))
    
    return page_info

class MenuNavigationMiddleWare(object):
    def _get_current_menu_from_url_path(self, url_path):
        regex_all = re.compile('[-\w]+')
        url_list = regex_all.findall(url_path)
        url_len = len(url_list)
        menu = CMSMenu.objects.get_menu(url_list[0] if url_len >= 1 else None)
        submenu = CMSMenu.objects.get_submenu(menu.slug if menu else None
                                              ,url_list[1] if url_len >= 2 else None)

        if not submenu:
            extrapath = url_list[1:]
        else:
            extrapath = url_list[2:]
        
        return menu, submenu, extrapath
                
    def _get_current_menu_from_url_path2(self, url_path):
        regex_all = re.compile('[-\w]+')
        url_list = regex_all.findall(url_path)
        url_len = len(url_list)
        request_extrapath = url_list[2:]
        if url_len >= 1:
            if url_len >= 2:
                url_len = 2
                                        
            def get_parent():
                if url_len == 2:
                    return url_list[0]
                return None
            
            menu = CMSMenu.objects.get_submenu(get_parent(),url_list[url_len-1])
            if not menu and url_len == 2:
                menu = CMSMenu.objects.get_submenu(None,url_list[0])
                request_extrapath = [url_list[1]] + request_extrapath

            return menu, request_extrapath
        return None
    
    def process_request(self, request):
        menu, submenu, request.cms_menu_extrapath = self._get_current_menu_from_url_path(request.path)
        request.test = {'bob': 'testing request'}
        context = {}
        cms_selected_menu = submenu if submenu else menu
        if cms_selected_menu and hasattr(menu, 'get_controller'):
            request.current_page = _get_page_parameters(cms_selected_menu.content_object)
            request.cms_selected_menu = cms_selected_menu
            request.cms_menu = menu
            request.cms_submenu = submenu
            request.cms_basepath = "/%s/%s/" % (menu.slug, submenu.slug)
        
            controller = cms_selected_menu.get_controller()
            if controller:
                return controller(request)
        request.cms_selected_menu = None
        return None
