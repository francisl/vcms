# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.db import models

class ContentManager(models.Manager):
    def get_contents_for_page(self, page=None):
        if page == None or page == "":
            return []
        else:
            return self.filter(page=page)
        