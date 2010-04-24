# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 21-04-2010.

from vcms.apps.simpleannouncements.feeds import AnnouncementRssFeed, AnnouncementCategoryRssFeed #AnnouncementCategoryAtom1Feed
from vcms.apps.simplenews.models import News
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class NewsRssFeed(AnnouncementRssFeed):
    model = News

    def title(self, obj):
        return _("News")

    def description(self):
        return _("Latest news site-wide.")

    def link(self):
        return reverse("vcms.apps.simplenews.views.news.recent.rss")

class NewsCategoryRssFeed(AnnouncementCategoryRssFeed):
    model = News

    def title(self, obj):
        return _("News")

    def description(self, obj):
        if len(obj) > 0:
            name = obj[0].category.name
            return _("Latest news for %s." % name)
        else:
            return ""

    def link(self, obj):
        if len(obj) > 0:
            slug = obj[0].category.slug
            return reverse("vcms.apps.simplenews.views.newscategory.recent.rss", kwargs={ "category_slug": slug })
        else:
            return ""


#class NewsCategoryAtomFeed(NewsCategoryRssFeed):
#    feed_type = AnnouncementAtom1Feed
#    subtitle = NewsCategoryRssFeed.description
