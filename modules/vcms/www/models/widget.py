# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.template.loader import render_to_string

# http://github.com/jpwatts/django-positions
from positions.fields import PositionField
from positions import PositionManager

#from vcms.www.managers.widget import ContentManager
from vcms.www.models.containers import TableContainer, GridContainer, RelativeContainer
from vcms.www.models.page import BasicPage


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
        raise NotImplementedError()

    def render(self):
        """ Renders the widget and returns the resulting HTML produced. """
        return self.widget.render()

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
        
    def __unicode__(self):
        return 'Widget - ' + self.widget.name

class GridWidgetWrapper(WidgetWrapper):
    container = models.ForeignKey(GridContainer, related_name="widgets")
    position = models.IntegerField(unique=True)

    class Meta:
        app_label = 'www'
        verbose_name = "Widget Wrapper - Grid"
        verbose_name_plural = "Widget Wrapper - Grid"

    def __unicode__(self):
        return 'Widget - ' + self.widget.name

class RelativeWidgetWrapper(WidgetWrapper):
    container = models.ForeignKey(RelativeContainer, related_name="widgets")
    position = models.IntegerField(unique=False)

    class Meta:
        app_label = 'www'
        verbose_name = "Widget Wrapper - Relative"
        verbose_name_plural = "Widget Wrapper - Relative"
        ordering = ['position']
    
    def __unicode__(self):
        return self.container.page.name + 'Widget - ' + self.widget.name

# -----------------
# WIDGETS
# -----------------
class Widget(models.Model):
    """ Widgets Parent class
        Contain all information required for all widget
        Make sure that a render method is override (to provide html)
    """
    MESURE_CHOICES = ((0, "px")
                     ,(1, "em")
                     ,(2, "%")
                     )
    
    name = models.CharField(max_length="40", help_text="Max 40 characters")
    width = models.FloatField(default=200)
    width_mesure = models.IntegerField(default=0, choices=MESURE_CHOICES)
    height = models.FloatField(default=0)
    height_mesure = models.IntegerField(default=0, choices=MESURE_CHOICES)
    
    class Meta:
        abstract = True
        app_label = 'www'
        
    def __unicode__(self):
        return self.id

    def render(self):
        raise NotImplementedError()

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


# -----------------
# CONTENT
# -----------------
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
                   ,'width': self.get_width()
                   ,'style': self.style
                   }
        return render_to_string("widget/content.html", content)
    
    class Meta:
        verbose_name= "Widget - Text"
        verbose_name_plural = "Widget - Text"
        ordering = ['date']
        app_label = 'www'
    
    def __unicode__(self):
        return self.__class__.__name__ + ' ' + self.content[:16]

    def get_page_where_available(self):
        try:
            thiswidget = RelativeWidgetWrapper.objects.filter(widget_id=self.id)[0]
            return thiswidget.container.page.get_absolute_url()
        except:
            return None

# -----------------
# CONTENT
# -----------------
from haystack.indexes import *
from haystack import site

class TextWidgetIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content = CharField(model_attr='content')
    page = CharField(model_attr='get_page_where_available')
    
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return TextWidget.objects.filter(published=True)


site.register(TextWidget, TextWidgetIndex)
