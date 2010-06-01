# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models

from vcms.apps.www.managers.containers import BasicContainerManager
from vcms.apps.www.managers.containers import GridContainerManager
from vcms.apps.www.models.widget import GridWidget

class BasicContainer(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_('Max 100 characters.'))

    objects = BasicContainerManager()

    class Meta:
        app_label = 'www'

class FloatContainer(BasicContainer):
    pass



class GridContainer(BasicContainer):
    gird_widget = models.ManyToManyField(GridWidget)
    
    objects = GridContainerManager()
    
    
    