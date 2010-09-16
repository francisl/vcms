# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from vcms.www.models.page import Page
from vcms.www.models import Language
#from vcms.news.managers import NewsCategoryManager

# Application connection to CMS
APP_SLUGS = "news"

class NewsCategory(models.Model):
    name = models.CharField(max_length="40", help_text=_("Max 40 characters"))

    # get live news
    def get_live_news(self):
        return self.news_set.filter(status=News.LIVE_STATUS)
    
    class Meta:
        verbose_name_plural = _("News Categories")

    def __unicode__(self):
        return self.name

class NewsPage(Page):
    categories = models.ManyToManyField(NewsCategory)

    class Meta:
        verbose_name_plural = "Pages - News"

    def save(self):
        self.module = 'News'
        self.app_slug = APP_SLUGS
        super(NewsPage, self).save()


class News(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = ((LIVE_STATUS, _('Live')), (DRAFT_STATUS, _('Draft')), (HIDDEN_STATUS, _('Hidden')))
    date = models.DateTimeField(auto_now=True, editable=True)
    name = models.CharField(max_length="40", help_text="Max 40 characters", verbose_name="Title")
    excerpt = models.TextField(verbose_name="Preview")
    content = models.TextField()
    language = models.ForeignKey(Language, default=Language.objects.get_default())
    categories = models.ManyToManyField(NewsCategory)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text=_("Only Entries with 'live' status will be publicly displayed"))
    
    try:
        from vimba_cms_simthetiq.apps.products.models import Image as p_Image
        from vimba_cms_simthetiq.apps.products.models import Video as p_Video
        product_images = models.ManyToManyField(p_Image, blank=True)
        product_videos = models.ManyToManyField(p_Video, blank=True)
    except:
        # no product
        pass
        
    class Meta:
        verbose_name_plural = _("News")
        ordering = ['-date']
        
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/news/" + str(self.id)
    
    def get_images_preview(self):
        return self.product_images.all()[:3]
                
    def get_videos_preview(self):
        return self.product_videos.all()[:3]

from vcms.www.models import PageElementPosition

class NewsPageModule(PageElementPosition):
    from vcms.www.models.page import DashboardPage as DP
    page = models.ForeignKey(DP)
    categories = models.ManyToManyField(NewsCategory)
    title = models.CharField(max_length="60")
    show_image_preview = models.BooleanField(default=False, help_text=_("Only if image are available to display"))
    show_video_preview = models.BooleanField(default=False, help_text=_("Only if video are available to display"))
    
    def __unicode__(self):
        return self.page.name

