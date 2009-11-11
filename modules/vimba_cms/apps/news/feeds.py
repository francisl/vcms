# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from vimba_cms.apps.news import models

#current_site = Site.objects.get_current()


class LatestEntriesFeed(Feed):
    author_name = "test"
    copyright = "%s" % "Simthetiq" #current_site.name
    description = "Latest test entries"
    feed_type = Atom1Feed
    item_copyright = "test Copyright"
    item_author_name = "test"
    item_author_link = "http://%s/" % "simthetiq.com" #current_site.domain
    link = "/news/feeds/entries"
    title = "%s: Latest entries" % 'simthetiq' #current_site.name
    
    def items(self):
        return models.News.objects.all()[:15]
    
    def item_pubdate(self, item):
        return item.date
    
    def item_guid(self, item):
        return "tag:%s,%s:%s" % ("simthetiq.com", #current_site.domain,
                                 item.data.strftime('%Y-%m-%d'),
                                 item.get_absolute_url())
        
    def item_categories(self, item):
        return [c.title for c in item.categories.all()]
    
