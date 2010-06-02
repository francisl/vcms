# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from vcms.apps.www.managers.widget import ContentManager
from vcms.apps.www.models.containers import FloatContainer, GridContainer


class WidgetWrapper(models.Model):
    # Generic FK to the widget, used as an inheritance workaround
    widget_type = models.ForeignKey(ContentType)
    widget_id = models.PositiveIntegerField()
    widget = generic.GenericForeignKey('widget_type', 'widget_id')

    class Meta:
        abstract = True


class GridWidgetWrapper(WidgetWrapper):
    container = models.ForeignKey(GridContainer)
    row = models.IntegerField()
    col = models.IntegerField()
    row_span = models.IntegerField()
    col_span = models.IntegerField()
    
    class Meta:
        app_label = 'www'
        
    def __unicode__(self):
        return widget.name


class FloatWidgetWrapper(WidgetWrapper):
    container = models.ForeignKey(FloatContainer)
    position = models.IntegerField(unique=True)
    
    class Meta:
        app_label = 'www'
        
    def __unicode__(self):
        return widget.name
    

# -----------------
# WIDGETS
# -----------------
class Widget(models.Model):
    """ Widgets Parent class
        Contain all information required for all widget
        Make sure that a render method is override (to provide html)
    """
    WIDTH_CHOICES = ((0, _("px"))
                     ,(1, _("em"))
                     ,(2, _("%"))
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
class ContentWidget(Widget):
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
    
    objects = ContentManager()
    
    def render(self):
        content = { 'name': self.name
                   ,'content' : self.content
                   ,'width': self.width
                   ,'style': self.style
                   }
        render_to_response("widget/content.html", content)
    
    class Meta:
        verbose_name_plural = "Page content"
        ordering = [ 'date']
        app_label = 'www'
    
    def __unicode__(self):
        return self.name
