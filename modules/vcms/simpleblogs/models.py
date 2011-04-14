# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify

from tagging.fields import TagField
from tagging.models import Tag

#from custom_fields.models import CustomField
from site_language.models import Language
from vcms.www.models.page import BasicPage
from vcms.www.models.widget import Widget
from vcms.www.fields import StatusField
from vcms.simpleblogs.managers import PublishedBlogPageManager, BlogPageManager, PublishedNewsBlogPostManager, BlogPostCategoryManager
from htmltools.html import HtmlReduce

APP_SLUGS = "blogs"

class BlogPage(BasicPage):
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
    
    ARCHIVE_DELAY_DEFAULT = 0
    ARCHIVE_DELAY_3MONTH = 90
    ARCHIVE_DELAY_6MONTH = 180
    ARCHIVE_DELAY_1YEAR = 356
    ARCHIVE_DELAY_CHOICES = ((ARCHIVE_DELAY_DEFAULT, _('No archives'))
                             ,(ARCHIVE_DELAY_3MONTH, _('Three months'))
                             ,(ARCHIVE_DELAY_6MONTH, _('Six months'))
                             ,(ARCHIVE_DELAY_1YEAR, _('One year'))
                             )
    
    comments_allowed = models.BooleanField(default=True)
    authorized_users = models.ManyToManyField(User, blank=True, null=True)
    authorized_groups = models.ManyToManyField(Group, blank=True, null=True)
    number_of_post_per_page = models.PositiveIntegerField(default=5)
    
    
    listing_style = models.CharField(max_length=32, choices=TEMPLATE, default=TEMPLATE_DETAILED_LIST)
    type = models.CharField(max_length=12, choices=NEWS_BLOGS_TYPE, default=BLOGS_TYPE)
    display_navigation_in = models.CharField(max_length=32, choices=NAVIGATION, default=NAVIGATION_SIDE_NAVIGATION)
    
    rss_feed = models.BooleanField(default=True)
    feeds_icon_position = models.PositiveIntegerField(choices=FEEDS_ICON, default=FEEDS_ICON_HEADER)
    
    objects = BlogPageManager()
    published = PublishedBlogPageManager()
    
    class Meta:
        verbose_name = _("Page - News/Blog Page")
        verbose_name_plural = _("Page - News/Blog Pages")
        ordering = ['name']
        
    def save(self):
        self.app_slug = self.type
        super(BlogPage, self).save()
        
    def get_absolute_url(self):
        menus = self.menu.all()
        if menus:
            return "%s" % menus[0].get_absolute_url()
        return '/'
        
    def get_next_announcement(self):
        return self.get_next_by_date_published(status=StatusField.PUBLISHED)

    def get_previous_announcement(self):
        return self.get_previous_by_date_published(status=StatusField.PUBLISHED)

    def get_controller(self):
        from vcms.simpleblogs.views import BlogPageController
        return BlogPageController(self)

class BlogPostCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, default='en') #Language.objects.get_default_code())

    objects = BlogPostCategoryManager()
    class Meta:
        ordering = ['name']
        verbose_name_plural = _("News/Blog Posts Categories")
        
    def __unicode__(self):
        return self.name

    def get_quantity_in_category(self):
        raise NotImplemented
    
    def save(self):
        self.slug = slugify(self.name.lower())
        super(BlogPostCategory, self).save()

        
class BlogPost(models.Model):
    PREVIEW_SHORT = 1
    PREVIEW_MEDIUM = 2
    PREVIEW_LONG = 4
    PREVIEW_LENGTH = ((1, _('Short'))
                      ,(2, _('Medium'))
                      ,(4, _('Long'))
                      )
    title = models.CharField(max_length=120)
    category = models.ManyToManyField(BlogPostCategory)
    description = models.CharField(max_length=240)
    content = models.TextField()
    
    preview = models.TextField(help_text=_('Display in widget or for post information and summary'), blank=True, editable=False)
    preview_length = models.PositiveIntegerField(choices=PREVIEW_LENGTH, default=PREVIEW_SHORT)
    
    status = StatusField()
    language = models.ForeignKey(Language, default='en') #Language.objects.get_default_code())
    display_on_page = models.ForeignKey(BlogPage)
    
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_published = models.DateTimeField(blank=True, null=True)
    
    objects = PublishedNewsBlogPostManager()
    published = PublishedNewsBlogPostManager()
    
    def _get_title(self):
        return self.title
    name = property(_get_title) # for search
    
    def get_page_where_available(self):
        return self.get_absolute_url()

    class Meta:
        verbose_name_plural = _("News/Blog Posts")
        get_latest_by = ['-date_created']
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "%s%s/%s/%s/%d/" % (self.display_on_page.get_absolute_url(), self.date_published.strftime("%Y"), self.date_published.strftime("%m"), self.date_published.strftime("%d"), self.id )

    def get_url(self):
        return  "/%s/%s/%s/%d/" % (self.date_published.strftime("%Y"), self.date_published.strftime("%m"), self.date_published.strftime("%d"), self.id )
    
    def save(self):
        self.preview = "<div>" + HtmlReduce(self.content, self.preview_length).get_html() + "</div>"
        
        # If the status has been changed to published, then set the date_published field so that we don't reset the date of a published page that is being edited
        now = datetime.datetime.now()
        self.date_modified = now
        if self.date_published == None:
            self.date_published = now

        super(BlogPost, self).save() 
    
    def get_fields(self):
        return dict([(field.name, field.value) for field in self.customfield_set.all()])

class CustomField(models.Model):
    name = models.CharField(max_length=120)
    value = models.TextField()
    post = models.ForeignKey(BlogPost)
    
    @staticmethod
    def get_fiels_for_page(self, page):
        return dict([(field.name, field.value) for field in self.objects.filter(page_set=page)])

    def __unicode__(self):
        return '%s : %s' % (self.name, self.value)


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
        page_url = self.page.get_absolute_url()
        if page_url:
            return "%s%s/" % (page_url, self.display_category.slug )
        return ''
