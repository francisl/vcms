# encoding: utf-8
# copyright Vimba inc. 2011
# programmer : Francis Lavoie

import re

from vcms.www.models.menu import CMSMenu

def _get_page_parameters(page=None):
    """ Set the default parameter for a CMS page 
        module , menu_style, current_page, page
    """
    page_info = { 'module' : None, 'current_page' : page }
    page_info.update(menu_style = CMSMenu.DROPDOWN_MENU)
    
    if page:
        page_info.update(module = page.module)
    
    return page_info

class MenuNavigationMiddleWare(object):
    def _get_current_menu_from_url_path(self, url_path):
        # TODO : exclude static or urelated path from querying the DB
        regex_all = re.compile('[-\w]+')
        url_list = regex_all.findall(url_path)
        #print('find all %s' % str(regex_all.findall(url_path)))
        url_len = len(url_list)
        if url_len >= 1:
            if url_len >= 2:
                url_len = 2
                                        
            def get_parent():
                if url_len == 2:
                    return url_list[0]
                return None
                
            return CMSMenu.objects.get_menu_from_string(get_parent(), url_list[url_len-1])
        return None
    
    def process_request(self, request):
        menu = self._get_current_menu_from_url_path(request.path)
        context = {}
        if menu and hasattr(menu, 'get_controller'):
            current_page = menu.content_object
            request.current_page = _get_page_parameters(current_page)

            request.cms_selected_menu = menu
        
            controller = menu.get_controller()
            if controller:
                return controller(request)
        request.cms_selected_menu = None
        return None
