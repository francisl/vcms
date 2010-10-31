# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from vcms.www.fields import StatusField
from django.conf import settings
from django.http import Http404

from site_language.models import Language

class BasicPageManager(models.Manager):
    def get_children(self, parent=None):
        if parent:
            return self.filter(parent=parent).filter(status=StatusField.PUBLISHED).filter(display=True)
        else:
            return None

    def get_default_page(self):
        return self.get_published()[0] #mm.content_object
    
    def get_all_basic(self):
        return self.filter(language=Language.objects.get_default())

    def get_main_published(self):
        return self.filter(status=StatusField.PUBLISHED).filter(level=0)

    def get_published(self):
        return self.filter(status=StatusField.PUBLISHED)

    def drafts(self):
        return self.filter(status=StatusField.DRAFT)

    def get_pages(self, lang='en'):
        lang = Language.objects.get_language(lang)
        return self.get_published().filter(language=lang)
        
    def get_containers(self):
        raise NotImplementedError
        
    def get_page_or_404(self, slug, app_slug):
        page = self.get_pages().filter(slug=slug).filter(app_slug=app_slug)
        if len(page) == 0:
            raise Http404
        return page[0]

"""
class ContentManager(models.Manager):
    def get_contents_for_page(self, page=None):
        if page == None or page == "":
            return []
        else:
            return self.filter(page=page)
"""