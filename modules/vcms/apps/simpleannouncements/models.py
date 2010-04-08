# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 26-03-2010.

from django.db import models
from tagging.fields import TagField
from vcms.apps.www.models import Page


APP_SLUGS = "simpleannouncements"


class Announcement(Page):
    content = models.TextField()
    comments_allowed = models.BooleanField(default=True)
    tags = TagField()
