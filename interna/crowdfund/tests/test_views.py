from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone

import pytest
from model_mommy import mommy

from crowdfund import models


@pytest.mark.django_db
@pytest.mark.parametrize(['method', 'url', 'pk', 'user', 'status_code'], [
    ('GET', 'crowdfund:index', None, None, 200),
    ('POST', 'crowdfund:index', None, None, 405),

    ('GET', 'crowdfund:detail', 1, None, 200),
    ('GET', 'crowdfund:detail', 999, None, 404),
    ('POST', 'crowdfund:detail', 1, None, 200),  # Creating new promises is OK

    ('GET', 'crowdfund:edit', 1, None, 302),  # Redirect to login
    ('GET', 'crowdfund:edit', 1, 1, 200),
    ('GET', 'crowdfund:edit', 2, 1, 403),
    ('GET', 'crowdfund:edit', 1, 2, 403),
    ('GET', 'crowdfund:edit', 999, 1, 404),
    ('POST', 'crowdfund:edit', 1, None, 302),  # Redirect to login
    ('POST', 'crowdfund:edit', 1, 1, 200),
    ('POST', 'crowdfund:edit', 2, 1, 403),
    ('POST', 'crowdfund:edit', 1, 2, 403),
    ('POST', 'crowdfund:edit', 999, 1, 404),
])
def test_status_codes(client, method, url, pk, user, status_code):
    """
    Make sure that login is required to modify data.
    """
    # Create models
    u1 = get_user_model().objects.create_user(pk=1, username='user', password='1234')
    get_user_model().objects.create_user(pk=2, username='user2', password='1235')

    # PK 1: Ongoing project by user 1
    mommy.make(models.Project, pk=1, image=None, initiator=u1, funded=None)

    # PK 2: Funded project by user 1
    mommy.make(models.Project, pk=2, image=None, initiator=u1, funded=timezone.now())

    # Login
    if user == 1:
        assert client.login(username='user', password='1234')
    elif user == 2:
        assert client.login(username='user2', password='1235')

    # Request
    reversed_url = reverse(url) if pk is None else reverse(url, kwargs={'pk': pk})
    response = getattr(client, method.lower())(reversed_url)
    assert response.status_code == status_code
