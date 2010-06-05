# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from vcms.apps.www.models.page import BasicPage
from vcms.apps.www.managers.containers import BasicContainerManager
from vcms.apps.www.managers.containers import GridContainerManager

class BasicContainer(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_('Max 100 characters.'))
    page = models.ForeignKey(BasicPage)

    objects = BasicContainerManager()

    class Meta:
        abstract = True
        app_label = 'www'


class FloatContainer(BasicContainer):
    ORIENTATION_CHOICES = (('left', _('Left'))
                           ,('right', _('Right'))
                           )
    float_orientation = models.CharField(max_length=10, default=ORIENTATION_CHOICES[0], choices=ORIENTATION_CHOICES)
    class Meta:
        app_label = 'www'


class GridContainer(BasicContainer):
    maximum_column = models.PositiveIntegerField(default=3, help_text="How many column are available")
    
    objects = GridContainerManager()
    class Meta:
        app_label = 'www'


class RelativeContainer(BasicContainer):
    class Meta:
        app_label = 'www'

    def render(self):
        content = { 'widgets': self.widgets }
        render_to_response("containers/relative.html", content)
