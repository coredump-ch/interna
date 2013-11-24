# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from django.db import models

from model_utils import Choices

from . import managers
from . import validators


class Member(models.Model):
    """A member of the association."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=100, blank=True,
        help_text='Wohnort')
    twitter = models.CharField(max_length=32, blank=True,
        help_text='Twitter Benutzername')
    github = models.CharField(max_length=32, blank=True,
        help_text='Github Benutzername')

    class Meta:
        ordering = ('name', 'id')

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    """A membership, with a start and end date.

    This is needed as a 1:n relation because a person can leave the association
    and then re-join later on.

    """
    CATEGORY = Choices(
        (1, 'verdiener', 'Verdiener'),
        (2, 'nichtverdiener', 'Nichtverdiener'),
    )

    Member = models.ForeignKey(Member, related_name='Membership')
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY, null=True)

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
        if not self.end:
            parts.append('since')
        parts.append('{}'.format(self.start))
        if self.end:
            parts.append('to {}'.format(self.end))
        return ' '.join(parts)


class MemberPayment(models.Model):
    """A membership payment by a member, linked to a calendar year."""
    Membership = models.ForeignKey(Membership, related_name='MemberPayment')
    year = models.CharField(max_length=4, validators=[validators.range_validator(int, 2000, 3000)])
    payment_date = models.DateField()
    amount = models.FloatField()

    def __unicode__(self):
        return '{} / {}'.format(self.year, self.Membership.Member.name)
