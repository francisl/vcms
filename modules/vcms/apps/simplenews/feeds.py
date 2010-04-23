# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 21-04-2010.

from vcms.apps.simpleannouncements.feeds import AnnouncementRssFeed #AnnouncementAtom1Feed
from vcms.apps.simplenews.models import News


class NewsCategoryRssFeed(AnnouncementRssFeed):
    model = News
    title = "News"
    link = "" # _TODO
    description = "" # _TODO

    def item_description(self, obj):
        return obj.content


#class NewsCategoryAtomFeed(NewsCategoryRssFeed):
#    feed_type = AnnouncementAtom1Feed
#    subtitle = NewsCategoryRssFeed.description
