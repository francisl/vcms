from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('vimba_cms_simthetiq.apps.order.views',
        (r'^/$', 'Order'),
        (r'orderform/$', 'OrderForm'),
        #(r'^validation/$', 'validation'),
        (r'confirmation/$', 'Confirm'),
)
