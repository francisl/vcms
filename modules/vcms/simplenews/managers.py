# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 27-03-2010.

from django.db import models
from django.db.models import Q


class NewsManager(models.Manager):
    def get_news_for_user(self, user):
        """
            Returns the News instances associated to the given user.
            A superuser can view all News instances.
        """
        if user.is_superuser:
            return self.all()
        return self.filter(Q(category__authorized_users=user) | Q(category__authorized_groups__in=user.groups.all())).distinct()


class NewsCategoryManager(models.Manager):
    def get_categories_in_use(self):
        """
            Returns the NewsCategory instances which are associated
            to published news instances.
        """
        from vcms.simplenews.models import News
        return self.filter(pk__in=News.published.all().values("category__pk"))
