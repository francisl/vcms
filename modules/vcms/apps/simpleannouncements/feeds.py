# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 21-04-2010.

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from vcms.apps.simpleannouncements.models import Announcement
from vcms.apps.simpleannouncements.settings import ANNOUNCEMENTS_PER_FEED



class AnnouncementRssFeed(Feed):
    model = Announcement
    title = ""
    link = ""
    description = ""

    def get_object(self, request):
        return self.model.published.get_latest()

    def item_description(self, obj):
        return obj.content

    def item_link(self, obj):
        return obj.get_absolute_url()

    def items(self, obj):
        return obj[:ANNOUNCEMENTS_PER_FEED]


class AnnouncementCategoryRssFeed(AnnouncementRssFeed):
    def get_object(self, request, category_slug):
        return self.model.published.get_latest().filter(category__slug=category_slug)


class AnnouncementCategoryAtomFeed(AnnouncementCategoryRssFeed):
    feed_type = Atom1Feed
    subtitle = AnnouncementCategoryRssFeed.description
