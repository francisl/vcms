# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage, FileSystemStorage

from vcms.apps.www.managers import WidgetManager

class Widgets(models.Model):
    WIDTH_CHOICES = ((0, _("px"))
                     ,(1, _("em"))
                     ,(2, _("%"))
                     )
    width = models.FloatField()
    width_mesure = models.IntegerField(default=0, choices=WIDTH_CHOICES)
    

    def __unicode__(self):
        return self.name

    def render(self):
        raise NotImplementedError() 
    