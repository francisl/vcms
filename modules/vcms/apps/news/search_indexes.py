
from haystack import indexes
from haystack import site
from vcms.apps.news.models import News


class NewsIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    content = indexes.CharField(model_attr='content')
    categories = indexes.CharField(model_attr='categories')
    
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return News.objects.filter(status=News.LIVE_STATUS)

site.register(News, NewsIndex)
