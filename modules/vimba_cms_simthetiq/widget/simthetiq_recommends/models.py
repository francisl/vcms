# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models

from positions.fields import PositionField
from positions import PositionManager

from vcms.www.models.containers import TableContainer, GridContainer, RelativeContainer
from vcms.www.models.menu import CMSMenu
from vcms.www.models import Widget

from django.template.loader import render_to_string

class PageLinksWidget(Widget):
    title = models.CharField(max_length=60)
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name= "Widget - Simthetiq Recommends"
        verbose_name_plural = "Widget - Simthetiq Recommends"
        ordering = ['title']
        app_label = 'www'

    def render(self):
        content = { 'title': self.title
                   ,'links': self.links.all().order_by('position')
                   ,'note': self.note
                   ,"name": self.name
                   ,"width": self.width
                   ,"width_mesure": self.get_width_mesure()
                   }
        return render_to_string("widget/pagelinks.html", content)

    def __unicode__(self):
        return self.title

class PageLink(models.Model):
    link = models.ForeignKey(CMSMenu)
    pagelink = models.ForeignKey(PageLinksWidget, related_name="links")
    position = PositionField(collection='pagelink')

    objects = PositionManager()

    class Meta:
        verbose_name= "Page Link"
        verbose_name_plural = "Page Link"
        ordering = ['link']
        app_label = 'www'

    def __unicode__(self):
        return self.link.name