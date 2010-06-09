# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models

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


class DashboardElementManager(models.Manager):
    def get_PublishedAll(self):
        return self.filter(published=True)

    def get_Published(self, current_page):
        return self.filter(published=True).filter(page=current_page)
