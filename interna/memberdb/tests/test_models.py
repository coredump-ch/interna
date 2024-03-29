from datetime import date

from pytest import mark
from model_bakery import baker

from .. import models


class TestMembershipModel:

    @mark.django_db
    def test_active_memberships(self):
        member = baker.make(models.Member)
        start = date(2013, 10, 10)
        baker.make(models.Membership, Member=member, start=start, end=None)
        baker.make(models.Membership, Member=member, start=start, end=date(2099, 10, 10))
        assert models.Membership.active.count() == 2
        assert models.Membership.expired.count() == 0

    @mark.django_db
    def test_inactive_memberships(self):
        member = baker.make(models.Member)
        start = date(2013, 10, 10)
        end = date(2013, 10, 12)
        baker.make(models.Membership, Member=member, start=start, end=end)
        assert models.Membership.active.count() == 0
        assert models.Membership.expired.count() == 1
