# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 21-04-2010.

from vcms.apps.simpleannouncements.feeds import AnnouncementCategoryRssFeed #AnnouncementCategoryAtom1Feed
from vcms.apps.simplenews.models import News


class NewsCategoryRssFeed(AnnouncementCategoryRssFeed):
    model = News
    title = "News"
    link = "" # _TODO
    description = "" # _TODO


#class NewsCategoryAtomFeed(NewsCategoryRssFeed):
#    feed_type = AnnouncementAtom1Feed
#    subtitle = NewsCategoryRssFeed.description
