# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from django.db import models


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

    class Meta:
        ordering = ('-start', '-Member__pk')

    def __unicode__(self):
        parts = []
        parts.append(self.Member.name)
        parts.append('{}'.format(self.start))
        if self.end:
            parts.append('to {}'.format(self.end))
        return ' '.join(parts)
