# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.utils.feedgenerator import Atom1Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory
from vcms.simpleblogs.models import APP_SLUGS

class LatestBlogFeed(Feed):
    author_name = settings.SITE_NAME
    copyright = "%s" % settings.SITE_NAME
    feed_type = Rss201rev2Feed
    item_copyright = "%s Copyright" % settings.SITE_NAME 
    
    def get_object(self, bits) :
        if len(bits) < 1 :
            raise ObjectDoesNotExist
        return BlogPage.objects.get_blog_page_from_string(bits[0])
    
    def link(self, obj) :
        return obj.get_absolute_url()
    
    def description(self, obj) :
        return _("%s - Latest blog entries") %settings.SITE_NAME
    
    def title(self, obj):
        return "%s Latest blog post for '%s'" % (settings.SITE_NAME, obj.name)
    
    def items(self, obj) :
        return BlogPost.published.get_latest_post_for_page(obj, 15)
    
    def item_pubdate(self, item):
        return item.date_published
    
    def item_guid(self, item):
        return "tag:%s,%s:%s" % ("simthetiq.com", #current_site.domain,
                                 item.date_published.strftime('%Y-%m-%d'),
                                 item.get_absolute_url())
        
    def item_categories(self, item):
        return [c.name for c in item.category.all()]
    
class CategoryFeed(LatestBlogFeed):
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
    