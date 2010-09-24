# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

import inspect
import sys

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from vcms.www.models.page import BasicPage
from vcms.www.managers.containers import PageContainerManager
from vcms.www.managers.containers import ContainerWidgetsManager
from vcms.www.managers.containers import BasicContainerManager
from vcms.www.managers.containers import TableContainerManager
from vcms.www.managers.containers import RelativeContainerManager
from vcms.www.managers.containers import GridContainerManager

CONTAINER_TYPE= (('relative' ,"Relative"),('table' ,"Table"),('absolute' ,"Absolute"))

class PageContainer(models.Model):
    container_name = models.CharField(max_length=100, unique=False, help_text=_('Max 100 characters.'))
    page = models.ForeignKey(BasicPage)
    container_type = models.CharField(max_length=20, choices=CONTAINER_TYPE, default=CONTAINER_TYPE[0])
    objects = PageContainerManager()

    class Meta:
        app_label = 'www'
        verbose_name = "Container - Page"
        verbose_name_plural = "Container - Pages"
        
    def __unicode__(self):
        return self.page.name + " - " + self.container_type + " - " + self.container_name
        
    def get_widgets(self):
        return ContainerWidgets.objects.filter(container=self)

class ContainerWidgets(models.Model):
    widget_type = models.ForeignKey(ContentType)
    widget_id = models.PositiveIntegerField()
    widget = generic.GenericForeignKey('widget_type', 'widget_id')

    container = models.ForeignKey(PageContainer, related_name="page_container")

    objects = ContainerWidgetsManager()

    #style
    css_style = models.CharField(max_length=200, null=True, blank=True)

    #table positionning
    table_row = models.PositiveIntegerField(default=0)
    table_col = models.PositiveIntegerField(default=0)
    table_row_span = models.PositiveIntegerField(default=0)
    table_col_span = models.PositiveIntegerField(default=0)

    #Static positionning
    absolute_top = models.IntegerField(blank=True, null=True)
    absolute_bottom = models.IntegerField(blank=True, null=True)
    absolute_left = models.IntegerField(blank=True, null=True)
    absolute_right = models.IntegerField(blank=True, null=True)
        
    #Relativ positionning
    relative_position = models.PositiveIntegerField(default=1)
    

    class Meta:
        app_label = 'www'
        verbose_name = "Container - Widget"
        verbose_name_plural = "Container - Widgets"

    def __unicode__(self):
        return self.widget.name
                
    def get_style(self):
        style = ""

        if self.container.container_type == 'absolute':
            style="position: absolute; "
            if self.absolute_top >= 0:
                style += "top : %spx; " % self.absolute_top
            if self.absolute_bottom >= 0:
                style += "bottom : %spx; " % self.absolute_bottom
            if self.absolute_left >= 0:
                style += "left : %spx; " % self.absolute_left
            if self.absolute_right >= 0:
                style += "right : %spx; " % self.absolute_right
        return style
        
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
        container_name = self.name
        # If the current container has its name set as the one of the required
        # containers for a type of page, then display its formatted name instead
        # of its internal name.
        if self.name in self.page.get_type().get_page_containers():
            container_name = self.page.get_type().get_page_containers()[self.name].name
        return unicode(self.page.name) + "("+ unicode(self.id) + ") - " + unicode(container_name)

    def get_type(self):
        """
            Returns the class of the current container.
            Used as a workaround to Django's ORM inheritance vs OOP's inheritance.
        """
        # Get all the classes in the current module
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            # Discard everything but classes and classes that inherit from BasicContainer
            if inspect.isclass(obj) and BasicContainer in obj.__bases__:
                # If there are instances for the current container, the instance is of
                # the current container's type
                if obj.objects.filter(pk=self.pk).exists():
                    return obj
        return BasicContainer


class ContainerDefinition:
    """ Class used to associate a display name to a container type. """
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

    def render(self):
        content = { 'float_orientation': self.float_orientation,
                    'widgets': self.widgets.all()
                    }
        return render_to_string("containers/grid.html", content)

class TableContainer(BasicContainer):
    maximum_column = models.PositiveIntegerField(default=3, help_text="How many column are available")
    
    objects = TableContainerManager()
    
    class Meta:
        app_label = 'www'
        verbose_name = "Container - Table"
        verbose_name_plural = "Container - Table"

    def render(self):
        content = { 'widgets': self.widgets.all() }
        return render_to_string("containers/table.html", content)

class RelativeContainer(BasicContainer):
    objects = RelativeContainerManager()
    
    class Meta:
        app_label = 'www'
        verbose_name = "Container - Relative"
        verbose_name_plural = "Container - Relative"

    def render(self):
        content = { 'widgets': self.widgets.all() }
        return render_to_string("containers/relative.html", content)

