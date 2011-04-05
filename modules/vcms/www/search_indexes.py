
from haystack import indexes
from haystack import site
from vcms.www.models.page import SimplePage, MainPage


class SimplePageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    content = indexes.CharField(model_attr='description')
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    keywords = indexes.CharField(model_attr='keywords')

class MainPageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    content = indexes.CharField(model_attr='description')
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    keywords = indexes.CharField(model_attr='keywords')


site.register(SimplePage, SimplePageIndex)
site.register(MainPage, MainPageIndex)
