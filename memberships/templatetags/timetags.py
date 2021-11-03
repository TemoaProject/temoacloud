from django import template
import datetime
register = template.Library()


def print_timestamp(timestamp):
    try:
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.date.fromtimestamp(ts)


register.filter(print_timestamp)