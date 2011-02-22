# encoding: utf-8
# copyright Vimba inc. 2011
# programmer : Francis Lavoie

from mockito import mock, when, spy, verify

from django.test import TestCase
from django.http import HttpRequest
from django.contrib.contenttypes.models import ContentType

from vcms.menu_navigation.middleware import MenuNavigationMiddleWare
from vcms.www.models.page import SimplePage
from site_language.models import Language

class PageFactory(object):
    def __init__(self):
        self.pages = []
        
    def create_simple_page_factory(self, page_slug):
        spage = SimplePage(name='%s' % page_slug
                       ,status=1
                       ,description='%s' % page_slug
                       ,slug='%s' % page_slug
                       ,language=Language.objects.get_default()
                       )
        spage.save()
        self.pages.append(spage)
        
        return spage

    def tearDown(self):
        for page in self.pages:
            page.delete()
    

class PageModelTest(TestCase):
    def setUp(self):
        self.page_factory = PageFactory()
        self.page = self.page_factory.create_simple_page_factory('testing1')

    def tearDown(self):
        self.page_factory.tearDown()

    def test_simplepage_get_controller_should_return_the_simple_controller_use_to_generate_the_simple_page(self):
        from vcms.www.views.html import simple_page
        self.assertEqual(simple_page, self.page.get_controller())
