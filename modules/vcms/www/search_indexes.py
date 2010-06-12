
from haystack import indexes
from haystack import site
from vcms.www.models.page import SimplePage, DashboardPage


class SimplePageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    keywords = indexes.CharField(model_attr='keywords')

class DashboardPageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    keywords = indexes.CharField(model_attr='keywords')


site.register(SimplePage, SimplePageIndex)
site.register(DashboardPage, DashboardPageIndex)
