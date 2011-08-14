# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.


ANNOUNCEMENTS_PER_FEED = 5

INSTALLED_APPS = (
    'django.contrib.comments', # http://docs.djangoproject.com/en/dev/ref/contrib/comments/
    'django.contrib.sites', # Required by django.contrib.comments
    'tagging', # http://code.google.com/p/django-tagging/
)
