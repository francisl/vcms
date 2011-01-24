# -*- coding: UTF8 -*-
# Application : CMS
# Module : Products
# Copyright (c) 2011 Vimba inc. All rights reserved.
# Created by Francis Lavoie on Jan 22 2011.

from django.test import TestCase
#from django.core.files import File as DjangoFile
#from mockito import *

from site_language.models import Language
from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory
#from vcms.simpleblogs.views import generate_html_paginator, get_page_items


class SimpleblogsPostTests(TestCase):
    def setUp(self):
        #self.lang = Language.objects.all()[0]
        pass
        
    def tearDown(self):
        #self.lang.delete()
        pass