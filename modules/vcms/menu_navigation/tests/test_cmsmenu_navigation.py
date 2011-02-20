# encoding: utf-8
# copyright Vimba inc. 2011
# programmer : Francis Lavoie

from mockito import mock, when, spy, verify

from django.test import TestCase
from django.http import HttpRequest
from django.contrib.contenttypes.models import ContentType

from vcms.menu_navigation.middleware import MenuNavigationMiddleWare
from vcms.www.models.menu import CMSMenu, MenuLocalLink
from vcms.www.tests.test_cmsmenu import MenuFactory
from site_language.models import Language

class MenuNavigationMiddleWareTest(TestCase):
    def setUp(self):
        self.mock_httprequest = mock(HttpRequest())
        self.menu_factory = MenuFactory()
        self.menu, self.menu2, self.locallink, self.menu_navigation_middleware = self.menu_factory.create_menu_factory()

    def tearDown(self):
        self.menu_factory.clean_menu_factory()

    def test_middleware_should_return_none_if_it_dont_find_the_menu_in_url(self):
        self.mock_httprequest.path = '/sapin/noel/'
        self.assertEqual(None, self.menu_navigation_middleware.process_request(self.mock_httprequest))

    def test_middleware__get_current_menu_from_url_path_should_return_the_parent_menu(self):
        menu = self.menu_navigation_middleware._get_current_menu_from_url_path('/testing_menu/')
        self.assertEqual(menu, self.menu)

    def test_middleware__get_current_menu_from_url_path_should_return_the_submenu_when_second_parameter(self):
        menu = self.menu_navigation_middleware._get_current_menu_from_url_path('/testing_menu/testing_menu2/')
        self.assertEqual(menu, self.menu2)
        
    def test_middleware__get_current_menu_from_url_path_should_return_the_submenu_when_second_parameter_and_more_are_present(self):
        menu = self.menu_navigation_middleware._get_current_menu_from_url_path('/testing_menu/testing_menu2/patate/au/riz')
        self.assertEqual(menu, self.menu2)

    def test_middleware_should_return_call_the_menu_related_method_when_found(self):
        self.mock_httprequest.path = "/testing_menu/"
        menu = self.menu_navigation_middleware._get_current_menu_from_url_path('/testing_menu/')
        spy_cmsmenu = spy(menu)
        verify(spy_cmsmenu).get_controller()

