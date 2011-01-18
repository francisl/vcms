
from haystack import indexes
from haystack import site
from vcms.simpleblogs.models import BlogPost


class NewsBlogsIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True, model_attr='content')
    name = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    keywords = indexes.CharField(model_attr='preview')
    pub_date = DateTimeField(model_attr='date_published')

site.register(BlogPost, NewsBlogsIndex)
