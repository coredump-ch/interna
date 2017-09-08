import pytest
from model_mommy import mommy

from crowdfund.models import Project, FundingPromise


@pytest.mark.django_db
def test_empty_project():
    p = mommy.make(Project, image=None, amount_required=500)
    assert p.amount_funded() == 0
    assert p.percent_funded() == 0
    assert len(p.active_promises()) == 0
    assert len(p.expired_promises()) == 0
    assert len(p.all_promises()) == 0


@pytest.mark.django_db
def test_regular_project():
    p1 = mommy.make(Project, image=None, amount_required=500)
    p2 = mommy.make(Project, image=None, amount_required=800)
    mommy.make(FundingPromise, project=p1, amount=100, expiry_date=None)
    mommy.make(FundingPromise, project=p1, amount=200, expiry_date=None)
    mommy.make(FundingPromise, project=p2, amount=400, expiry_date=None)
    assert p1.amount_funded() == 300
    assert p2.amount_funded() == 400
    assert p1.percent_funded() == 60
    assert p2.percent_funded() == 50
    assert len(p1.active_promises()) == 2
    assert len(p2.active_promises()) == 1
    assert len(p1.expired_promises()) == 0
    assert len(p2.expired_promises()) == 0
    assert len(p1.all_promises()) == 2
    assert len(p2.all_promises()) == 1
