# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q

from . import managers


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ('name', 'id')

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    Member = models.ForeignKey(Member, related_name='Membership')
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    # Custom managers
    objects = models.Manager()
    active = managers.MembershipActivityManager(active=True)
    expired = managers.MembershipActivityManager(active=False)

    class Meta:
        ordering = ('-start', '-Member__pk')
        get_latest_by = ('end', 'start')

    def __unicode__(self):
        parts = []
        parts.append(self.Member.name)
        parts.append('{}'.format(self.start))
        if self.end:
            parts.append('to {}'.format(self.end))
        return ' '.join(parts)
