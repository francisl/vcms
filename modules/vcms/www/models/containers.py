# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from django.template.loader import render_to_string
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
        if GridContainer.objects.filter(pk=self.pk).exists():
            return GridContainer
        elif TableContainer.objects.filter(pk=self.pk).exists():
            return TableContainer
        elif RelativeContainer.objects.filter(pk=self.pk).exists():
            return RelativeContainer
        else:
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
        content = { 'widgets': self.widgets.all() }
        return render_to_string("containers/relative.html", content)

