# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from vcms.www.models.page import BasicPage
from vcms.www.models.containers import ContainerWidgets
# -----------------
# WIDGETS
# -----------------
class Widget(models.Model):
    """ Widgets Parent class
        Contain all information required for all widget
        Make sure that a render method is override (to provide html)
    """
    name = models.CharField(max_length="40", help_text="Max 40 characters")
    
    class Meta:
        abstract = True
        app_label = 'www'
        
    def __unicode__(self):
        return self.id

    def render(self):
        raise NotImplementedError()


# -----------------
# CONTENT
# -----------------
class TextWidget(Widget):
    #CONTENT
    excerpt = models.TextField(verbose_name="Preview")
    content = models.TextField()

    #appearance
    TEXT_ONLY = 0
    BOXED = 1
    DARK = 2
    AVAILABLE_STYLES = ((TEXT_ONLY, _('Text only'))
                 ,(BOXED, _('Box'))
                 ,(DARK, _('Bright text on dark background'))
                 )
    style = models.IntegerField(default=TEXT_ONLY, choices=AVAILABLE_STYLES)
    
    #INFORMATION
    date = models.DateField(auto_now=True, editable=True)
    author = models.ForeignKey(User, related_name='content_author', editable=False, null=True, blank=True)
    
    #objects = ContentManager()
    
    def render(self):
        content = { 'name': self.name
                   ,'content' : self.content
                   ,'style': self.style
                   }
        return render_to_string("widget/content.html", content)
    
    class Meta:
        verbose_name= "Widget - Text"
        verbose_name_plural = "Widget - Text"
        ordering = ['date']
        app_label = 'www'
    
    def __unicode__(self):
        return self.__class__.__name__ + ' : ' + self.name

    def get_page_where_available(self):
        try:
            thiswidget = ContainerWidgets.objects.filter(widget_id=self.id)[0]
            return thiswidget.container.page.get_absolute_url()
        except:
            return None

# -----------------
# CONTENT SEARCH
# -----------------
from haystack.indexes import *
from haystack import site

class TextWidgetIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content = CharField(model_attr='content')
    page = CharField(model_attr='get_page_where_available')
    
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return TextWidget.objects.all()
        
site.register(TextWidget, TextWidgetIndex)
