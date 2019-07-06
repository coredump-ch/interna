from typing import Optional

from django.urls import reverse

import pytest
from model_mommy import mommy

from inventory import views
from inventory.models import Item


def query_index_by_category(rf, category: Optional[str]):
    if category is None:
        request = rf.get(reverse('inventory:index'))
    else:
        request = rf.get('{}?category={}'.format(reverse('inventory:index'), category))
    response = views.Index.as_view()(request)
    assert response.status_code == 200
    response.render()
    html = response.content.decode('utf8')
    return html


@pytest.mark.django_db
def test_filtering(rf):
    mommy.make(Item, name='C64', category='vintage')
    mommy.make(Item, name='Apple II', category='vintage')
    mommy.make(Item, name='Ultimaker', category='manufacturing')
    mommy.make(Item, name='Unknown', category=None)

    # List all elements
    html = query_index_by_category(rf, category=None)
    assert 'Aktuell sind 4 Objekte' in html
    assert '>C64<' in html
    assert '>Apple II<' in html
    assert '>Ultimaker<' in html
    assert '>Unknown<' in html

    # Filter by category
    html = query_index_by_category(rf, category='vintage')
    assert 'Aktuell sind 2 Objekte' in html
    assert '>C64<' in html
    assert '>Apple II<' in html
    assert '>Ultimaker<' not in html
    assert '>Unknown<' not in html
    html = query_index_by_category(rf, category='manufacturing')
    assert 'Aktuell ist 1 Objekt' in html
    assert '>C64<' not in html
    assert '>Apple II<' not in html
    assert '>Ultimaker<' in html
    assert '>Unknown<' not in html

    # Filter with no category
    html = query_index_by_category(rf, category='none')
    assert 'Aktuell ist 1 Objekt' in html
    assert '>C64<' not in html
    assert '>Apple II<' not in html
    assert '>Ultimaker<' not in html
    assert '>Unknown<' in html
