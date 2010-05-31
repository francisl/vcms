# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage, FileSystemStorage
from django.shortcuts import render_to_response

from vcms.apps.www.managers import WidgetManager

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

    def __unicode__(self):
        return self.id

    def render(self):
        raise NotImplementedError() 
    
class GridWidget(models.Model):
    widget = models.OneToOneField(Widget)
    row = models.IntegerField()
    col = models.IntegerField()
    row_span = models.IntegerField()
    col_span = models.IntegerField()
    
    def __unicode__(self):
        return widget.name
    
class FloatWidget(models.Model):
    widget = models.OneToOneField(Widget)
    position = models.IntegerField(unique=True)
    
    def __unicode__(self):
        return widget.name
    
# -----------------
# WIDGETS
# -----------------

# -- CONTENT
# ----------
class Content(Widget):
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
    author = models.ForeignKey(User, editable=False, null=True, blank=True)
    
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
        ordering = [ 'position', 'date']
    
    def __unicode__(self):
        return self.name
