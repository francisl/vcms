# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from vcms.www.models.page import BasicPage
from vcms.www.managers.containers import ContainerWidgetsManager
from vcms.www.fields import StatusField

class ContainerWidgets(models.Model):
    MESURE_CHOICES = ((0, "px")
                     ,(1, "em")
                     ,(2, "%")
                     )
    FLOAT_CHOICES = (('float: left;', "Left")
                      ,('clear: both;', "Clear")
                      ,('float: right;', "Right")
                      )
    
    page = models.ForeignKey(BasicPage)   
    container = models.CharField(max_length=80, default=BasicPage.containers[0][0], choices=BasicPage.containers)
    
    widget_type = models.ForeignKey(ContentType)
    widget_id = models.PositiveIntegerField()
    widget = generic.GenericForeignKey('widget_type', 'widget_id')

    status = models.IntegerField(default=StatusField.PUBLISHED, choices=StatusField.STATUSES)

    objects = ContainerWidgetsManager()

    width = models.FloatField(default=200)
    width_mesure = models.IntegerField(default=MESURE_CHOICES[0], choices=MESURE_CHOICES)
    height = models.FloatField(default=0)
    height_mesure = models.IntegerField(default=MESURE_CHOICES[0], choices=MESURE_CHOICES)

    #style
    float_position = models.CharField(max_length=40, default=FLOAT_CHOICES[1], choices=FLOAT_CHOICES)
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
        if self.page.containers_type.get(self.container) == 'absolute':
            style="position: absolute; "
            if self.absolute_top >= 0:
                style += "top : %spx; " % self.absolute_top
            if self.absolute_bottom >= 0:
                style += "bottom : %spx; " % self.absolute_bottom
            if self.absolute_left >= 0:
                style += "left : %spx; " % self.absolute_left
            if self.absolute_right >= 0:
                style += "right : %spx; " % self.absolute_right
        style += '%s' % self.css_style 
        style += "width: %s%s" % (self.width, self.MESURE_CHOICES[self.width_mesure][1])
        return style
        
    def get_width(self):
        if self.width > 0:
            return str(self.width) + self.MESURE_CHOICES[self.width_mesure][1]
        return "none"

    def get_width_mesure(self):
        return self.MESURE_CHOICES[self.width_mesure][1]

    def get_height(self):
        if self.height > 0:
            return str(self.height) + self.MESURE_CHOICES[self.height_mesure][1]
        return "none"

    def get_absolute_url(self):
        return self.page.get_absolute_url()
