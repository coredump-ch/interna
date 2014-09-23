# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import datetime

from django.db import models
from django.db.models import Q


class MembershipActivityManager(models.Manager):

    def __init__(self, active, *args, **kwargs):
        super(MembershipActivityManager, self).__init__(*args, **kwargs)
        self.active = active

    def get_query_set(self):
        qs = super(MembershipActivityManager, self).get_query_set()
        today = datetime.today()
        if self.active:
            return qs.filter(Q(start__lte=today), Q(end__gt=today) | Q(end__isnull=True))
        else:
            return qs.filter(end__isnull=False, end__lte=today)
