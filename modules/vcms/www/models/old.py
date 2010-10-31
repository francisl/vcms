# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.

import datetime

from vcms.www.managers import ContentManager

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from vcms.www.models.page import BasicPage
from site_language.models import Language

# -- CONTENT
# ----------

class Content(models.Model):
    #CONTENT
    name = models.CharField(max_length="40", help_text="Max 40 characters")
    excerpt = models.TextField(verbose_name="Preview")
    content = models.TextField()
    published = models.BooleanField(default=False)

    #position
    POSITION_HELP_TEXT = _("Supported value are 'Default', px, em or %")
    width = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    height = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    margin_top = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    margin_left = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    position = models.IntegerField(default=5, help_text="Priority to display. 0=top, 9=bottom")

    #appearance
    TEXT_ONLY = 0
    BOXED = 1
    DARK = 2
    AVAILABLE_STYLES = ((TEXT_ONLY, _('Text only'))
                 ,(BOXED, _('Box'))
                 ,(DARK, _('Bright text on dark background'))
                 )
    style = models.IntegerField(default=TEXT_ONLY, choices=AVAILABLE_STYLES)
    minimized = models.BooleanField(default=False, choices=((True, _('Minimized')),(False, _('Show'))))

    #INFORMATION
    date = models.DateField(auto_now=True, editable=True)
    author = models.ForeignKey(User, editable=False, null=True, blank=True)
    #page = models.ForeignKey(BasicPage)

    objects = ContentManager()

    class Meta:
        verbose_name_plural = "Page content"
        ordering = [ 'position', 'date']
        app_label = "www"
        

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        self.page.get_absolute_url()

