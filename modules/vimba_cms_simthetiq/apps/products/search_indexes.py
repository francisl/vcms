from django.conf import settings
from haystack import indexes
from haystack import site
from vimba_cms_simthetiq.apps.products.models import ProductPage


# Get the search index according to the current environment
search_index = getattr(indexes, settings.SEARCH_INDEX)

class ProductPageIndex(search_index):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    keywords = indexes.CharField(model_attr='keywords')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return ProductPage.objects.all()


site.register(ProductPage, ProductPageIndex)
