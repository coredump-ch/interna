from datetime import date

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

import pytest
from model_mommy import mommy

from memberdb import models
from front import views


@pytest.mark.django_db
def test_members_view(rf):
    """
    Regression test for #10.

    As a side effect, this also tests #9.

    """
    m = mommy.make(models.Member, name='Fritzli Meier')
    u = mommy.make(get_user_model(), is_staff=True, is_superuser=True)
    mommy.make(models.Membership, Member=m, start=date(2014, 7, 12), end=date(2015, 9, 16))
    mommy.make(models.Membership, Member=m, start=date(2016, 1, 1), end=None)

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
    assert '<h3>Aktivmitglieder (1)</h3>' in html
    assert '<h3>Ehemalige Mitglieder (0)</h3>' in html
