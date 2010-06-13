# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

#from vcms.www.managers.widget import ContentManager
from vcms.www.models.containers import TableContainer, GridContainer, RelativeContainer


class WidgetWrapper(models.Model):
    # Generic FK to the widget, used as an inheritance workaround
    widget_type = models.ForeignKey(ContentType)
    widget_id = models.PositiveIntegerField()
    widget = generic.GenericForeignKey('widget_type', 'widget_id')

    class Meta:
        abstract = True
        verbose_name = "Widget Wrapper"
        verbose_name_plural = "Widget Wrappers"

    def __unicode__(self):
        return 'Widget - ' + self.widget.name


class TableWidgetWrapper(WidgetWrapper):
    container = models.ForeignKey(TableContainer, related_name="widgets")
    row = models.IntegerField()
    col = models.IntegerField()
    row_span = models.IntegerField()
    col_span = models.IntegerField()
    
    class Meta:
        app_label = 'www'
        verbose_name = "Widget Wrapper - Table"
        verbose_name_plural = "Widget Wrapper - Table"

class GridWidgetWrapper(WidgetWrapper):
    container = models.ForeignKey(GridContainer, related_name="widgets")
    position = models.IntegerField(unique=True)

    class Meta:
        app_label = 'www'
        verbose_name = "Widget Wrapper - Grid"
        verbose_name_plural = "Widget Wrapper - Grid"


class RelativeWidgetWrapper(WidgetWrapper):
    container = models.ForeignKey(RelativeContainer, related_name="widgets")
    position = models.IntegerField(unique=False)

    class Meta:
        app_label = 'www'
        verbose_name = "Widget Wrapper - Relative"
        verbose_name_plural = "Widget Wrapper - Relative"


# -----------------
# WIDGETS
# -----------------
class Widget(models.Model):
    """ Widgets Parent class
        Contain all information required for all widget
        Make sure that a render method is override (to provide html)
    """
    WIDTH_CHOICES = ((0, "px")
                     ,(1, "em")
                     ,(2, "%")
                     )
    
    name = models.CharField(max_length="40", help_text="Max 40 characters")
    width = models.FloatField()
    width_mesure = models.IntegerField(default=0, choices=WIDTH_CHOICES)
    
    class Meta:
        abstract = True
        app_label = 'www'
        
    def __unicode__(self):
        return self.id

    def render(self):
        raise NotImplementedError()


# -- CONTENT
# ----------
class TextWidget(Widget):
    #CONTENT
    excerpt = models.TextField(verbose_name="Preview")
    content = models.TextField()
    published = models.BooleanField(default=False)

    #appearance
    TEXT_ONLY = 0
    BOXED = 1
    DARK = 2
    AVAILABLE_STYLES = ((TEXT_ONLY, _('Text only'))
                 ,(BOXED, _('Box'))
                 ,(DARK, _('Bright text on dark background'))
                 )
    style = models.IntegerField(default=TEXT_ONLY, choices=AVAILABLE_STYLES)
    #minimized = models.BooleanField(default=False, choices=((True, _('Minimized')),(False, _('Show'))))
    
    #INFORMATION
    date = models.DateField(auto_now=True, editable=True)
    author = models.ForeignKey(User, related_name='content_author', editable=False, null=True, blank=True)
    
    #objects = ContentManager()
    
    def render(self):
        content = { 'name': self.name
                   ,'content' : self.content
                   ,'width': str(self.width)+str(self.WIDTH_CHOICES[self.width_mesure][1])
                   ,'style': self.style
                   }
        return render_to_string("widget/content.html", content)
    
    class Meta:
        verbose_name= "Widget - Text"
        verbose_name_plural = "Widget - Text"
        ordering = [ 'date']
        app_label = 'www'
    
    def __unicode__(self):
        return self.name