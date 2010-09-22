# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models


class PageContainerManager(models.Manager):
    def get_containers_for_page(self, page):
        return self.filter(page=page)

    def get_container_for_page_of_type(self, page, type, container_name):
        return self.filter(page=page).filter(container_type=type).filter(container_name=container_name)
        
class ContainerWidgetsManager(models.Manager):
    def get_widgets_for_container(self, container):
        return self.filter(container=container)

class BasicContainerManager(models.Manager):
    def get_widgets(self):
        raise NotImplementedError

class RelativeContainerManager(BasicContainerManager):
    def get_widgets(self):
        return self.relative_widget.all()
    
class TableContainerManager(BasicContainerManager):
    def get_widgets(self):
        return self.table_widget.all()
    
class GridContainerManager(BasicContainerManager):
    def get_widgets(self):
        return self.grid_widget.all()

## TODO: to remove
class DashboardElementManager(models.Manager):
    def get_PublishedAll(self):
        return self.filter(published=True)

    def get_Published(self, current_page):
        return self.filter(published=True).filter(page=current_page)
