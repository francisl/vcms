# encoding: utf-8
# copyright Vimba inc. 2011
# programmer : Francis Lavoie

import re

from vcms.www.models.menu import CMSMenu

class MenuNavigationMiddleWare(object):
    def _get_current_menu_from_url_path(self, url_path):
        regex_all = re.compile('[-\w]+')
        url_list = regex_all.findall(url_path)
        #print('find all %s' % str(regex_all.findall(url_path)))
        url_len = len(url_list)
        if url_len >= 1:
            if url_len > 2:
                url_len = 2
            return CMSMenu.objects.get_menu_from_string(url_list[url_len-1])
        return None
    
    def process_request(self, request):
        menu = self._get_current_menu_from_url_path(request.path)
        if menu:
            menu.content_object.get_controller()
        return None
