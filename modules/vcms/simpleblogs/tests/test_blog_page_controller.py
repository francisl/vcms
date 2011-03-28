# -*- coding: utf-8 -*-
# Application : CMS
# Module : Products
# Copyright (c) 2011 Vimba inc. All rights reserved.
# Created by Francis Lavoie on Jan 22 2011.

import types

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, Http404

from mockito import mock, when, spy, verify

from vcms.simpleblogs.views import BlogPageController, page
from vcms.simpleblogs.models import BlogPage
from site_language.models import Language

class dummyBlogPage(object):
    def slug(self):
        return ''
            
class BlogPageControllerTest(TestCase):
    def setUp(self):
        self.mock_request = mock(HttpRequest)
        self.mock_request.path = '/blog/'
        self.mock_request.GET = {}
        self.mock_request.method = 'GET'
        self.mock_request.cms_menu_extrapath = []
        self.lang = Language(language='english', language_code='en')
        self.lang.save()
        self.bp = BlogPage(name='testpage'
                           ,slug='testpage'
                           ,description='testpage'
                           ,status=1
                           ,language=self.lang)
        self.bp.save()

    def tearDown(self):
        del self.mock_request
        self.lang.delete()

    def test_asked_for_archives_should_return_false_when_not_specified(self):
        bpc = BlogPageController(dummyBlogPage())
        self.assertEqual(bpc.is_requesting_archived(['bob']), False)

    def test_asked_for_archives_should_return_True_when_first_parameter_equal_to_archives(self):
        bpc = BlogPageController(dummyBlogPage())
        self.assertEqual(bpc.is_requesting_archived(['archives']), True)
        
    def test___call___should_return_an_archives_page_if_extra_path_startwith_archives(self):
        self.mock_request.cms_menu_extrapath = ['archives']
        def _call_page_for_archives(self, *args, **kargs):
            self.archives_called = True
        bpcn = BlogPageController(self.bp)
        setattr(bpcn, 'archives_called', False)
        f = types.MethodType(_call_page_for_archives, bpcn, BlogPageController)
        bpcn._call_page_for_archives = f
        bpcn(self.mock_request)
        self.assertTrue(bpcn.archives_called)

    def test___call___for_archives_with_page_get_parameter_should_return_an_archives_with_page_X(self):
        self.mock_request.cms_menu_extrapath = ['archives', 2009]
        self.mock_request.GET = {'page' : 2 }
        def _call_page_for_archives(self, *args, **kwargs):
            self.archives_called = True
            self.archives_for_page = kwargs['page_number']
        bpcn = BlogPageController(self.bp)
        setattr(bpcn, 'archives_called', False)
        setattr(bpcn, 'archives_for_year', False)
        bpcn._call_page_for_archives = types.MethodType(_call_page_for_archives, bpcn, BlogPageController)
        bpcn(self.mock_request)
        self.assertTrue(bpcn.archives_called)
        self.assertEqual(bpcn.archives_for_page, 2)

    def test___call___for_archives_with_too_many_parameter_should_raise_404(self):
        self.mock_request.cms_menu_extrapath = ['archives', 2009, 'category1', 'extra']
        bpcn = BlogPageController(self.bp)
        try:
            response = bpcn(self.mock_request)
        except :
            return
        self.assertTrue(False)

