# Django
import re

from django import template
register = template.Library()


@register.filter
def filer_tag(value):
    return (value[:15] + '..') if len(value) > 15 else value


regex = re.compile('[@!#$ %^&*()<>?/\|}{~:]')


def check_name(value):
    if regex.search(value) is None:
        return value

    else:
        new_string = re.sub(regex, '', value)
        return new_string
