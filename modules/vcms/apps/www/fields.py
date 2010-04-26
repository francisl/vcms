# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 26-04-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _


class StatusField(models.IntegerField):
    """
        IntegerField with predefined choice and default statuses.
    """
    DRAFT = 0
    PUBLISHED = 1
    STATUSES = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )

    def __init__(self, *args, **kwargs):
        # If the choices of default args have been given, then use them instead of the default ones
        if "choices" not in kwargs:
            kwargs["choices"] = StatusField.STATUSES
        if "default" not in kwargs:
            kwargs["default"] = StatusField.DRAFT
        super(StatusField, self).__init__(*args, **kwargs)
