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


class BlogPage(AnnouncementPage):
    NEWS_TYPE = "news"
    BLOGS_TYPE = "blogs"
    NEWS_BLOGS_TYPE = ((NEWS_TYPE, _('NEWS'))
                       ,(BLOGS_TYPE, _('BLOGS'))
                       )
    
    NAVIGATION_DISABLE = 'disable'
    NAVIGATION_SIDE_NAVIGATION = 'side_navigation'
    NAVIGATION_IN_PAGE_NAVIGATION = 'in_page_navigation'
    NAVIGATION = ((NAVIGATION_SIDE_NAVIGATION, _('Side navigation'))
                  ,(NAVIGATION_IN_PAGE_NAVIGATION, _('Inside Page navigation'))
                  ,(NAVIGATION_DISABLE, _('Disable'))
                  )
    
    FEEDS_ICON_DISABLE = 0
    FEEDS_ICON_HEADER = 1
    FEEDS_ICON_PAGE = 2
    FEEDS_ICON = ((FEEDS_ICON_DISABLE, _('Disable'))
                  ,(FEEDS_ICON_HEADER, _('In navigation header')) 
                  ,(FEEDS_ICON_PAGE, _('On page'))
                  )
    
    TEMPLATE_SHORT_LIST = 'short_list'
    TEMPLATE_DETAILED_LIST = 'detailed_list'
    TEMPLATE = ((TEMPLATE_DETAILED_LIST, _('Detailed List'))
                ,(TEMPLATE_SHORT_LIST, _("Short List"))
                )
    objects = BlogPageManager()
    published = PublishedBlogPageManager()
    listing_style = models.CharField(max_length=32, choices=TEMPLATE, default=TEMPLATE_DETAILED_LIST)
    type = models.CharField(max_length=12, choices=NEWS_BLOGS_TYPE, default=BLOGS_TYPE)
    display_navigation_in = models.CharField(max_length=32, choices=NAVIGATION, default=NAVIGATION_SIDE_NAVIGATION)
    feeds_icon_position = models.PositiveIntegerField(choices=FEEDS_ICON, default=FEEDS_ICON_HEADER)
    
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
        verbose_name= "Widget - News/Blog Preview"
        verbose_name_plural = "Widget - News/Blogs Preview"

    def __unicode__(self):
        return self.__class__.__name__ + ' ' + self.name

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (APP_SLUGS, self.page.slug, self.display_category.slug )

#class NewsBlogNavigationWidget(Widget):
#    page = models.ForeignKey(BlogPage)
#
#    def render(self, current_page=None):
#        from vcms.simpleblogs.views import get_side_menu
#        categories, archives, older_archives = get_side_menu(self.page)
#        template = "newsblogs_navigation.html"
#        widget =  render_to_string(template
#                                   ,{'page': self.page
#                                     ,'categories': categories
#                                     ,'archives':archives
#                                     ,'older_archives': older_archives })
#        return widget
#
#    class Meta:
#        verbose_name= "Widget - News/Blog Navigation"
#        verbose_name_plural = "Widget - News/Blogs Navigation"
#
#    def __unicode__(self):
#        return self.__class__.__name__ + ' ' + self.name
#
#    def get_absolute_url(self):
#        return "/%s/%s/%s/" % (APP_SLUGS, self.page.slug, self.display_category.slug )

