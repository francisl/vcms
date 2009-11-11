# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from vimba_cms.apps.news.models import News, NewsCategory

#current_site = Site.objects.get_current()


class LatestNewsFeed(Feed):
    author_name = "test"
    copyright = "%s" % "Simthetiq" #current_site.name
    description = "Latest test entries"
    feed_type = Atom1Feed
    item_copyright = "test Copyright"
    item_author_name = "test"
    item_author_link = "http://%s/" % "simthetiq.com" #current_site.domain
    link = ""
    title = "%s: Latest entries" % 'simthetiq' #current_site.name
    
    def items(self):
        return News.objects.all()[:15]
    
    def item_pubdate(self, item):
        return item.date
    
    def item_guid(self, item):
        return "tag:%s,%s:%s" % ("simthetiq.com", #current_site.domain,
                                 item.date.strftime('%Y-%m-%d'),
                                 item.get_absolute_url())
        
    def item_categories(self, item):
        return [c.name for c in item.categories.all()]
    
class CategoryFeed(LatestNewsFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return NewsCategory.objects.get(name__exact=bits[0])
    
    def title(self, obj):
        return "%s Latest news in category '%s'" % ("Simthetiq", obj.name)
    
    def description(self, obj):
        return "%s: Latest news in category '%s'" % ("Simthetiq", obj.name)
    
    #def link(self, obj):
    #    return obj.get_absolute_url()
    
    def items(self, obj):
        return obj.get_live_news()[:15]
    