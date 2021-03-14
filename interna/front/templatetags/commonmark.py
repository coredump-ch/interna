import commonmark

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='commonmark')
def commonmark_filter(value):
    """
    Run a string through commonmark.

    Note: This will mark the string as safe. Since commonmark may contain
    arbitrary HTML, make sure that the input is safe, before applying this
    filter.
    """
    return mark_safe(commonmark.commonmark(value))
