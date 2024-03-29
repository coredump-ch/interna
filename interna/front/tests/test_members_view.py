import re
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from model_bakery import baker

from memberdb import models
from front import views


@pytest.mark.django_db
def test_members_view(rf):
    """
    Regression test for #10.

    As a side effect, this also tests #9.

    """
    m = baker.make(models.Member, name='Fritzli Meier')
    u = baker.make(get_user_model(), is_staff=True, is_superuser=True)
    baker.make(models.Membership, Member=m, start=date(2014, 7, 12), end=date(2015, 9, 16))
    baker.make(models.Membership, Member=m, start=date(2016, 1, 1), end=None)

    request = rf.get(reverse('front:members'))
    request.user = u
    request.session = {}
    response = views.MembersView.as_view()(request)
    assert response.status_code == 200

    # The name should only occur in the members list once
    response.render()
    html = response.content.decode('utf8')
    assert 'Fritzli Meier' in html
    assert html.count('Fritzli Meier') == 1

    # The member should be active
    assert re.search(r'<h3[^>]*>Aktivmitglieder \(1\)<\/h3>', html)
    assert re.search(r'<h3[^>]*>Ehemalige Mitglieder \(0\)<\/h3>', html)
