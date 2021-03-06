# -*- coding: utf-8 -*-
# Application : CMS
# Module : Products
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie on 10-11-20.

from django.test import TestCase
from django.core.files import File as DjangoFile

from mockito import *

from site_language.models import Language
from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory
from vcms.simpleblogs.views import generate_html_paginator, get_page_items

class GetPostedItemsForPagpeControllerTest(TestCase):
    def setUp(self):
        pass
        
        
    def test_get_pages_items_should_return_the_first_6_items(self):
        page_items = get_page_items(range(12), page_number=1, item_per_page=6)
        self.assertEqual(len(page_items), 6)
        self.assertEqual(page_items[0], 0)
        self.assertEqual(page_items[1], 1)
        self.assertEqual(page_items[2], 2)
        self.assertEqual(page_items[3], 3)
        self.assertEqual(page_items[4], 4)
        self.assertEqual(page_items[5], 5)
                
                
    def test_get_the_second_page_I_should_only_see_the_remaining_4_items(self):
        page_items = get_page_items(range(10), page_number=2, item_per_page=6)
        self.assertEqual(len(page_items), 4)
        self.assertEqual(page_items[0], 6)
        self.assertEqual(page_items[1], 7)
        self.assertEqual(page_items[2], 8)
        self.assertEqual(page_items[3], 9)
        
        
