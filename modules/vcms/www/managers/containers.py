# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from vcms.www.fields import StatusField

class ContainerWidgetsManager(models.Manager):
    def get_all(self, page):
        return self.order_by('relative_position').filter(page=page)
    
    def get_widgets(self, page, container):
        return self.get_all(page=page).filter(container=container)
        
    def get_published_widget(self, page, container):
        return self.get_all(page=page).filter(container=container).filter(status=StatusField.PUBLISHED)
    def get_page_for_widget(self, widget):
        containers = self.filter(widget_id=widget.id)
        if containers:
            return containers[0].page
        return None
        

class DashboardElementManager(models.Manager):
    def get_PublishedAll(self):
        return self.filter(published=True)

    def get_Published(self, current_page):
        return self.filter(published=True).filter(page=current_page)
