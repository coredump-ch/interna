from datetime import datetime

from django.core import mail

from freezegun import freeze_time
from model_bakery import baker
import pytest
import pytz

from crowdfund.models import Project, FundingPromise


@pytest.mark.django_db
def test_empty_project():
    with freeze_time('2017-01-01'):
        p = baker.make(Project, image=None, amount_required=500)
    assert p.amount_funded() == 0
    assert p.percent_funded() == 0
    assert len(p.active_promises()) == 0
    assert len(p.expired_promises()) == 0
    assert len(p.all_promises()) == 0
    assert p.created.isoformat() == '2017-01-01T00:00:00+00:00'


@pytest.mark.django_db
def test_regular_project():
    p1 = baker.make(Project, image=None, amount_required=500)
    p2 = baker.make(Project, image=None, amount_required=800)
    baker.make(FundingPromise, project=p1, amount=100, expiry_date=None)
    baker.make(FundingPromise, project=p1, amount=200, expiry_date=None)
    baker.make(FundingPromise, project=p2, amount=400, expiry_date=None)
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


@pytest.mark.django_db
def test_funded_freeze():
    with freeze_time('2017-01-01'):
        p1 = baker.make(Project, image=None, amount_required=120)
        assert p1.amount_funded() == 0
        assert p1.percent_funded() == 0
        assert p1.funded is None
        assert len(p1.active_promises()) == len(p1.expired_promises()) == 0

    # First promise without expiration
    with freeze_time('2017-01-02'):
        baker.make(FundingPromise, project=p1, amount=80, expiry_date=None)
        assert p1.amount_funded() == 80
        assert p1.percent_funded() == 66
        assert len(p1.active_promises()) == 1
        assert len(p1.expired_promises()) == 0

    # Second promise with expiration, not enough to trigger funding
    with freeze_time('2017-01-03'):
        baker.make(FundingPromise, project=p1, amount=30,
                expiry_date=datetime(2017, 1, 4, tzinfo=pytz.utc))
        assert p1.amount_funded() == 110
        assert p1.percent_funded() == 91

    # Expires two days later
    with freeze_time('2017-01-05'):
        assert p1.amount_funded() == 80
        assert p1.percent_funded() == 66
        assert p1.funded is None

    # Create a new expiring promise that reaches the funding goal
    with freeze_time('2017-01-05'):
        baker.make(FundingPromise, project=p1, amount=50,
                expiry_date=datetime(2017, 1, 7, tzinfo=pytz.utc))
        assert p1.amount_funded() == 130
        assert p1.funded == datetime(2017, 1, 5, tzinfo=pytz.utc)

    # It is still funded the next day, before the promise expires
    with freeze_time('2017-01-06'):
        assert p1.amount_funded() == 130
        assert p1.funded == datetime(2017, 1, 5, tzinfo=pytz.utc)

    # We can also add further promises
    with freeze_time('2017-01-07'):
        baker.make(FundingPromise, project=p1, amount=10,
                expiry_date=datetime(2017, 1, 8, tzinfo=pytz.utc))
        assert p1.amount_funded() == 140

    # This time, the promises do not expire because the funding was reached before
    with freeze_time('2017-01-09'):
        assert p1.amount_funded() == 140
        assert p1.percent_funded() == 116
        assert p1.funded == datetime(2017, 1, 5, tzinfo=pytz.utc)
        assert len(p1.active_promises()) == 3
        assert len(p1.expired_promises()) == 1


@pytest.mark.django_db
def test_funding_emails():
    p = baker.make(Project, image=None, amount_required=120,
            initiator__email='foo@bar.baz', title='Yolo')
    assert len(mail.outbox) == 0
    baker.make(FundingPromise, project=p, amount=80, expiry_date=None)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '80 CHF für dein Projekt "Yolo"!'
    baker.make(FundingPromise, project=p, amount=20, expiry_date=None)
    assert len(mail.outbox) == 2
    assert mail.outbox[1].subject == '20 CHF für dein Projekt "Yolo"!'
    baker.make(FundingPromise, project=p, amount=30, expiry_date=None)
    assert len(mail.outbox) == 4
    assert mail.outbox[2].subject == '30 CHF für dein Projekt "Yolo"!'
    assert mail.outbox[3].subject == 'Dein Projekt "Yolo" wurde finanziert!'
