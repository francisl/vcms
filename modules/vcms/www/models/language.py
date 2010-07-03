# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie


from django.db import models
from django.utils.translation import ugettext_lazy as _

from vcms.www.managers.page import LanguageManager

class Language(models.Model):
    language = models.CharField(max_length=50, help_text=_('Max 50 characters.'))
    language_code = models.CharField(max_length=2, primary_key=True, help_text=_('e.g. fr = French or en = english'))

    objects = LanguageManager()

    class Meta:
        app_label = "www"
        
    def __unicode__(self):
        return self.language
        
