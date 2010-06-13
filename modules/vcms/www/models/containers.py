# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from vcms.www.models.page import BasicPage
from vcms.www.managers.containers import BasicContainerManager
from vcms.www.managers.containers import TableContainerManager
from vcms.www.managers.containers import RelativeContainerManager
from vcms.www.managers.containers import GridContainerManager

class BasicContainer(models.Model):
    name = models.CharField(max_length=100, unique=False, help_text=_('Max 100 characters.'))
    page = models.ForeignKey(BasicPage)

    objects = BasicContainerManager()

    class Meta:
        abstract = True
        app_label = 'www'
        verbose_name = "Container - Basic"
        verbose_name_plural = "Container - Basic"
        
    def __unicode__(self):
        return self.page.name + " - " + self.name

class ContainerDefinition:
    """ Defines the human name associated to a container type. """
    name = _("Basic container")
    type = BasicContainer

    def __init__(self, name, type):
        self.name = name
        self.type = type

class GridContainer(BasicContainer):
    ORIENTATION_CHOICES = (('left', _('Left'))
                           ,('right', _('Right'))
                           )
    float_orientation = models.CharField(max_length=10, default=ORIENTATION_CHOICES[0], choices=ORIENTATION_CHOICES)
    class Meta:
        app_label = 'www'
        verbose_name = "Container - Grid"
        verbose_name_plural = "Container - Grid"

class TableContainer(BasicContainer):
    maximum_column = models.PositiveIntegerField(default=3, help_text="How many column are available")
    
    objects = TableContainerManager()
    
    class Meta:
        app_label = 'www'
        verbose_name = "Container - Table"
        verbose_name_plural = "Container - Table"


class RelativeContainer(BasicContainer):
    objects = RelativeContainerManager()
    
    class Meta:
        app_label = 'www'
        verbose_name = "Container - Relative"
        verbose_name_plural = "Container - Relative"

    def render(self):
        content = { 'widgets': self.widgets }
        render_to_response("containers/relative.html", content)