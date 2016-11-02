# -*- coding: utf-8 -*-


from django.core.exceptions import ValidationError


def range_validator(datatype, start, end):
    """Return a range validator.

    Asserts that the value is in ``range(start, end)``.

    Args:
        datatype:
            The datatype of the values (e.g. ``int`` or ``float``).
        start:
            The start of the range (inclusive).
        end:
            The end of the range (exclusive).

    Returns:
        Validation function.

    """
    def validate(value):
        value = datatype(value)
        if not (value >= start and value < end):
            raise ValidationError('Value must be between {} and {}.'.format(start, end))
    return validate
