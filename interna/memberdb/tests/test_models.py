# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import date

from pytest import mark

from .. import models


class TestMemberModel(object):

    @mark.django_db
    def test_active_membership(self):
        member = models.Member.objects.create(name='fritzli', email='fritzli@example.com')
        membership = models.Membership.objects.create(Member=member,
                start=date(2013, 10, 10), end=None)
        assert member.active_membership() == membership

    @mark.django_db
    def test_inactive_membership(self):
        member = models.Member.objects.create(name='fritzli', email='fritzli@example.com')
        membership = models.Membership.objects.create(Member=member,
                start=date(2013, 10, 10), end=date(2013, 10, 12))
        assert member.active_membership() is None
