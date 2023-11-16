from django.core.exceptions import ValidationError
import pytest

from inventory import models


@pytest.mark.django_db
def test_identifier_validation():
    item = models.Item()
    item.name = 'Foobar'
    item.owner = 'Der Foobär'

    errmsg = 'Bitte ein gültiges Kürzel, bestehend aus Buchstaben, Ziffern, ' + \
             'Unterstrichen und Bindestrichen, eingeben.'
    exception = "{'identifier': ['%s']}" % errmsg

    item.identifier = 'foo bar'
    with pytest.raises(ValidationError) as e:
        item.full_clean()
    assert str(e.value) == exception

    item.identifier = 'foobär'
    with pytest.raises(ValidationError) as e:
        item.full_clean()
    assert str(e.value) == exception

    item.identifier = 'foobar'
    item.full_clean()
