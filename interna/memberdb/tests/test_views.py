from datetime import date

from django.contrib.auth.models import User
from pytest import mark
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate

from .. import models, views


class TestMembershipView:

    @mark.django_db
    def test_active_members(self):
        # Test data: Create 3 members, 2 of them active
        start = date(2013, 10, 10)
        end = date(2013, 10, 12)
        member1_active = baker.make(models.Member)
        member2_active = baker.make(models.Member)
        member3_inactive = baker.make(models.Member)
        baker.make(models.Membership, Member=member1_active, start=start, end=None)
        baker.make(models.Membership, Member=member2_active, start=start, end=date(2099, 10, 10))
        baker.make(models.Membership, Member=member3_inactive, start=start, end=end)
        assert models.Membership.active.count() == 2
        assert models.Membership.expired.count() == 1

        # Test user
        user = baker.make(User, is_staff=True)

        # Create an API request
        factory = APIRequestFactory()
        view = views.ActiveMemberView.as_view()
        request = factory.get('api/members/active/')
        force_authenticate(request, user=user)

        # Validate response
        response = view(request)
        assert response.status_code == 200
        assert len(response.data) == 2
        members = [x['member']['id'] for x in response.data]
        assert members == [member1_active.id, member2_active.id]
        assert response.data[0]['membership']['start'] == '2013-10-10'
        assert response.data[0]['membership']['end'] is None
        assert response.data[1]['membership']['start'] == '2013-10-10'
        assert response.data[1]['membership']['end'] == '2099-10-10'

    @mark.django_db
    def test_auth_required(self):
        factory = APIRequestFactory()
        view = views.ActiveMemberView.as_view()
        request = factory.get('api/members/active/')
        response = view(request)

        assert response.status_code == 403
        assert response.data['detail'].code == 'not_authenticated'

    @mark.django_db
    @mark.parametrize('staff', [True, False])
    def test_admin_required(self, staff: bool):
        print(staff)
        user = baker.make(User, is_staff=staff)

        factory = APIRequestFactory()
        view = views.ActiveMemberView.as_view()
        request = factory.get('api/members/active/')
        force_authenticate(request, user=user)
        response = view(request)

        if staff:
            assert response.status_code == 200
        else:
            assert response.status_code == 403
            assert response.data['detail'].code == 'permission_denied'
