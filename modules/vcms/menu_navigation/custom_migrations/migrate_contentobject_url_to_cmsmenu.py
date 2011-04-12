# encoding: utf-8
# copyright Vimba inc. 2011
# programmer : Francis Lavoie

import re

from django.contrib.contenttypes.models import ContentType

from vcms.www.models.menu import CMSMenu
from vcms.www.models.page import SimplePage


"""
for menu in CMSMenu.objects.all():
    if hasattr(menu.content_object, 'slug'):
        menu.slug = menu.content_object.slug
        menu.save()
    if hasattr(menu.content_object, 'local_link'):
        link = menu.content_object.local_link.split('/')
        if len(link) > 3:
            if link[1] == 'www' and link[2] == 'page':
                menu.slug = link[3]
                old_link = menu.content_object
                ct = ContentType.objects.get_for_id(menu.content_object.id)
                menu.content_type = ct
                menu.object_id = menu.content_object.id
                menu.save()
                old_link.delete()
"""            

def run():
    for menu in CMSMenu.objects.all():
        if hasattr(menu.content_object, 'local_link'):
            link = menu.content_object.local_link.split('/')
            if len(link) > 3:
                if link[1] == 'www' and link[2] == 'page':
                    page = SimplePage.objects.get(slug=link[3])
                    menu.slug = link[3]
                    print("menu : %s | slug : %s | id : %s | page : %s" % (menu, menu.slug, menu.id, page))
                    old_link = menu.content_object
                    ct = ContentType.objects.get(app_label='www', model='simplepage')
                    print("Content id : %s, content name : %s" % (ct.id, ct))
                    menu.object_id = page.id
                    menu.content_type = ct
                    menu.save()
                #old_link.delete()
