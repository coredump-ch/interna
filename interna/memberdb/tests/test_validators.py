# -*- coding: utf-8 -*-


from django.core.exceptions import ValidationError

import pytest

from .. import validators


@pytest.mark.parametrize(('start', 'end', 'value', 'valid'), [
    (10, 20, 15, True),
    (10, 20, '15', True),
    (10, 20, 10, True),
    (10, 20, 19, True),
    (10, 20, 20, False),
    (10, 21, 20, True),
])
def test_range_validator(start, end, value, valid):
    v = validators.range_validator(int, start, end)
    if valid:
        try:
            v(value)
        except ValidationError as e:
            pytest.fail('Validation failed: {}'.format(e))
    else:
        with pytest.raises(ValidationError):
            v(value)
