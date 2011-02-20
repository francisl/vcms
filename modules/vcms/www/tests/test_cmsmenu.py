# encoding: utf-8
# copyright Vimba inc. 2011
# programmer : Francis Lavoie

from mockito import mock, when, spy, verify

from django.test import TestCase
from django.http import HttpRequest
from django.contrib.contenttypes.models import ContentType

from vcms.menu_navigation.middleware import MenuNavigationMiddleWare
from vcms.www.models.menu import CMSMenu, MenuLocalLink
from site_language.models import Language

class MenuFactory(object):
    def __init__(self):
        self.locallink = None
        self.menu = None
        
    def create_menu_factory(self):
        self.locallink = MenuLocalLink(name='testlink', local_link='/testing_menu/')
        self.locallink.save()
        locallink_type = ContentType.objects.get(app_label="www", model="menulocallink")
        self.menu_navigation_middleware = MenuNavigationMiddleWare()
        self.menu = CMSMenu(menu_name='Testing Menu'
                       ,display=True
                       ,slug='testing_menu'
                       ,language=Language.objects.get_default()
                       ,content_type=locallink_type
                       ,object_id=self.locallink.id
                       )
        self.menu.save()
        self.menu2 = CMSMenu(menu_name='Testing Menu2'
                       ,display=True
                       ,slug='testing_menu2'
                       ,language=Language.objects.get_default()
                       ,content_type=locallink_type
                       ,object_id=self.locallink.id
                       )
        self.menu2.save()
        return self.menu, self.menu2, self.locallink, self.menu_navigation_middleware

    def clean_menu_factory(self):
        self.menu.delete()
        self.menu2.delete()
        self.locallink.delete()
    

class CMSMenuManagerTest(TestCase):
    def setUp(self):
        self.menu_factory = MenuFactory()
        self.menu, self.menu2, self.locallink, self.menu_navigation_middleware = self.menu_factory.create_menu_factory()

    def tearDown(self):
        self.menu_factory.clean_menu_factory()
        
    def test_cmsmenu_objects_get_menu_for_string_should_return_the_model_instance_when_found(self):
        menu = CMSMenu.objects.get_menu_from_string('testing_menu')
        self.assertEqual(menu, self.menu)
        
    def test_cmsmenu_objects_get_menu_for_string_should_return_none_if_no_menu(self):
        self.assertEqual(CMSMenu.objects.get_menu_from_string('test'), None)

class CMSMenuModelTest(TestCase):
    def setUp(self):
        self.menu_factory = MenuFactory()
        self.menu, self.menu2, self.locallink, self.menu_navigation_middleware = self.menu_factory.create_menu_factory()

    def tearDown(self):
        self.menu_factory.clean_menu_factory()

    def test_get_controller_should_return_none_if_no_controller_are_associated_with_the_menu(self):
        self.assertEqual(None, self.menu.get_controller())
    
    def test_get_controller_should_return_the_function_that_will_handle_the_request(self):
        pass
