# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class LanguageManager(models.Manager):
    def get_default(self):
        return self.get(language_code=settings.LANGUAGE_CODE[:2])

    def get_default_code(self):
        return self.get(language_code=settings.LANGUAGE_CODE[:2]).language_code
        
    def get_default_for_choice(self):
        l = self.get(language_code=settings.LANGUAGE_CODE[:2])
        return (l.language, l.language_code)
        
    def get_available_language(self):
        return [(l.language, l.language_code) for l in self.all()]

    def get_language(self, string_value):
        try:
            return self.get(language_code=string_value)
        except:
            return self.get_default()


class Language(models.Model):
    DEFAULT = settings.LANGUAGE_CODE[:2]
    language = models.CharField(max_length=50, help_text=_('Max 50 characters.'))
    language_code = models.CharField(max_length=2, primary_key=True, help_text=_('e.g. fr = French or en = english'))

    objects = LanguageManager()
        
    def __unicode__(self):
        return self.language
        
