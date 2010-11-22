# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from django.template.loader import render_to_string

from vcms.www.models.widget import Widget
from vcms.simpleannouncements.models import AnnouncementPage, AnnouncementPost, AnnouncementPostCategory
from vcms.simpleblogs.managers import PublishedBlogPageManager, BlogPageManager, PublishedNewsBlogPostManager, BlogPostCategoryManager
from vcms.simpleannouncements.managers import PublishedAnnouncementPostManager
from tagging.models import Tag

APP_SLUGS = "blogs"

NEWS_TYPE = "news"
BLOGS_TYPE = "blogs"
NEWS_BLOGS_TYPE = ((NEWS_TYPE, _('NEWS'))
                   ,(BLOGS_TYPE, _('BLOGS'))
                   )

class BlogPage(AnnouncementPage):
    objects = BlogPageManager()
    published = PublishedBlogPageManager()
    type = models.CharField(max_length=12, choices=NEWS_BLOGS_TYPE, default=BLOGS_TYPE)
    
    class Meta:
        verbose_name = _("Page - News/Blog Page")
        verbose_name_plural = _("Page - News/Blog Pages")
        ordering = ['name']
        
    def save(self):
        self.app_slug = self.type
        super(BlogPage, self).save()

class BlogPostCategory(AnnouncementPostCategory):
    objects = BlogPostCategoryManager()
    class Meta:
        ordering = ['name']
        verbose_name_plural = _("News/Blog Posts Categories")
        
class BlogPost(AnnouncementPost):
    display_on_page = models.ForeignKey(BlogPage)
    category = models.ManyToManyField(BlogPostCategory)
    
    objects = PublishedNewsBlogPostManager()
    published = PublishedNewsBlogPostManager()
    
    class Meta:
        verbose_name_plural = _("News/Blog Posts")
        get_latest_by = ['-date_created']
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/%s/%s/%s/%d" % (APP_SLUGS, self.display_on_page.slug, self.date_published.strftime("%Y"), self.date_published.strftime("%m"), self.date_published.strftime("%d"), self.id )

    def save(self):
        import re
        reg = re.compile(r"<p(?:.*?)>(.*?)<\/p>")
        preview = ""
        all_found = reg.findall(self.content)
        for found in all_found[:self.preview_length]:
            preview += '<p>' + found + '</p>'
        self.preview = "<div>" + preview + "</div>"
        super(BlogPost, self).save() 
    

# -----------------
# CONTENT
# -----------------
class BlogPostWidget(Widget):
    page = models.ForeignKey(BlogPage)
    display_elements = models.PositiveIntegerField(default=2)
    display_category = models.ForeignKey(BlogPostCategory, null=True, blank=True, help_text=_("select nothings to display all categories"))
    display_image = models.BooleanField(default=True)
    
    WIDGET_TEMPLATE_SUMMARY_LIST = 1
    WIDGET_TEMPLATE_DETAILED = 2
    WIDGET_TEMPLATE = ((WIDGET_TEMPLATE_SUMMARY_LIST, _('Short List'))
                      ,(WIDGET_TEMPLATE_DETAILED, _('Detailed view'))
                      )

    display_template = models.PositiveIntegerField(choices=WIDGET_TEMPLATE, default=WIDGET_TEMPLATE_DETAILED)
    
    def render(self):
        posts = BlogPost.published.get_latest_post_for_page(self.page, qty=self.display_elements, category=self.display_category) #, self.display_elements)
        if self.display_template == self.WIDGET_TEMPLATE_SUMMARY_LIST:
            template = "newsblogs_widget/short_list.html"
        else: 
            template = "newsblogs_widget/detailed_view.html"
        widget =  render_to_string(template
                                    ,{ 'name': self.name, 'posts':posts, 'widget': self })
        return widget

    class Meta:
        verbose_name= "Widget - News/Blog"
        verbose_name_plural = "Widget - News/Blogs"

    def __unicode__(self):
        return self.__class__.__name__ + ' ' + self.name

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (APP_SLUGS, self.page.slug, self.display_category.slug )
