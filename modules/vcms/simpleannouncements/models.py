# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 26-03-2010.

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, User

from tagging.fields import TagField

from vcms.www.fields import StatusField
from vcms.www.models.page import BasicPage, STATUS_DRAFT, STATUS_PUBLISHED, STATUSES
from vcms.simpleannouncements.managers import PublishedAnnouncementPostManager
from vcms.www.models import Language

APP_SLUGS = "simpleannouncements"

class AnnouncementPage(BasicPage):
    comments_allowed = models.BooleanField(default=True)
    authorized_users = models.ManyToManyField(User, blank=True, null=True)
    authorized_groups = models.ManyToManyField(Group, blank=True, null=True)
    number_of_post_per_page = models.PositiveIntegerField(default=5)

    objects = models.Manager()
    
    class Meta:
        abstract = True

    def get_next_announcement(self):
        return self.get_next_by_date_published(status=StatusField.PUBLISHED)

    def get_previous_announcement(self):
        return self.get_previous_by_date_published(status=StatusField.PUBLISHED)

    def __unicode__(self):
        return self.name


class AnnouncementPostCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, default=Language.objects.get_default_code())

    class Meta:
        abstract = True
                
    def __unicode__(self):
        return self.name

    def get_quantity_in_category(self):
        raise NotImplemented
    

class AnnouncementPost(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    status = StatusField()
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_published = models.DateTimeField(auto_now=True, editable=False)
    language = models.ForeignKey(Language, default=Language.objects.get_default_code())
    
    published = PublishedAnnouncementPostManager()
    
    class Meta:
        """Default values. Will be inherited from children models even if the Meta class is redefined."""
        abstract = True
        verbose_name_plural = _("Announcement Posts")
        get_latest_by = ['-date_created']
        ordering = ['-date_created']

    def save(self):
        # If the status has been changed to published, then set the date_published field so that we don't reset the date of a published page that is being edited
        self.date_modified = datetime.datetime.now()
        if self.status == STATUSES[STATUS_PUBLISHED]:
            # If the post is being created, set its published date
            if not self.pk:
                self.date_published = self.date_modified
            # If the post is being edited, check against the current version in the database and update if it hasn't been previously published
            else:
                model_in_db = AnnouncementPost.objects.get(pk=self.pk)
                if model_in_db.status != StatusField.PUBLISHED:
                    self.date_published = self.date_modified

                    
        super(AnnouncementPost, self).save()
        
    def __unicode__(self):
        return self.title