# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 26-03-2010.

from django.db import models
from tagging.fields import TagField
from vcms.apps.www.models import Page
from vcms.apps.simpleannouncements.managers import PublishedAnnouncementManager, PublishedAnnouncementCategoryManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, User
import datetime


APP_SLUGS = "simpleannouncements"


class Announcement(models.Model):
    DRAFT = 0
    PUBLISHED = 1
    STATUSES = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )
    name = models.CharField(max_length=100, unique=True, help_text=_('Max 40 characters.'))
    slug = models.SlugField(max_length=150, unique=True, help_text=_("Used for hyperlinks, no spaces or special characters."))
    content = models.TextField()
    status = models.IntegerField(choices=STATUSES, default=DRAFT)
    comments_allowed = models.BooleanField(default=True)
    tags = TagField()
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_published = models.DateTimeField(default=datetime.datetime.min, editable=False)

    objects = models.Manager()
    published = PublishedAnnouncementManager()

    def get_next_announcement(self):
        return self.get_next_by_date_published(status=Page.PUBLISHED)

    def get_previous_announcement(self):
        return self.get_previous_by_date_published(status=Page.PUBLISHED)

    def __unicode__(self):
        return self.name

    def save(self):
        # If the status has been changed to published, then set the date_published field so that we don't reset the date of a published page that is being edited
        if self.status == self.PUBLISHED:
            # If the page is being created, set its published date
            if not self.pk:
                self.date_published = datetime.datetime.now()
            # If the Announcement is being edited, check against the current version in the database and update if it hasn't been previously published
            else:
                model_in_db = Announcement.objects.get(pk=self.pk)
                if model_in_db.status != self.PUBLISHED:
                    self.date_published = datetime.datetime.now()
        super(Announcement, self).save()


class AnnouncementCategory(Page):
    comments_allowed = models.BooleanField(default=True, help_text=_("This will be the default value when adding a new item."))
    authorized_users = models.ManyToManyField(User, related_name="announcement", blank=True, null=True)
    authorized_groups = models.ManyToManyField(Group, related_name="announcement", blank=True, null=True)

    published = PublishedAnnouncementCategoryManager()

    def __unicode__(self):
        return self.name

    class Meta:
        """Default values. Will be inherited from children models even if the Meta class is redefined."""
        verbose_name_plural = _("Announcement categories")
        get_latest_by = ['-date_created']
        ordering = ['name']
