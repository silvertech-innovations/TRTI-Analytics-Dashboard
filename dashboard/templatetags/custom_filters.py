from django import template
from datetime import datetime
import json

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get dictionary value by key
    Usage: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def format_date(date_value):
    """
    Format date to a readable string
    Usage: {{ date_value|format_date }}
    """
    if not date_value:
        return ""
    try:
        if isinstance(date_value, str):
            date_value = datetime.strptime(date_value, '%Y-%m-%d')
        return date_value.strftime('%d-%m-%Y')
    except:
        return date_value

@register.filter
def to_json(value):
    """
    Convert a value to JSON string
    Usage: {{ value|to_json }}
    """
    return json.dumps(value)

@register.filter
def default_if_none(value, default=""):
    """
    Return a default value if the input is None
    Usage: {{ value|default_if_none:"N/A" }}
    """
    return value if value is not None else default

@register.filter
def split(value, delimiter=','):
    """
    Split a string into a list
    Usage: {{ string_value|split:"," }}
    """
    if value:
        return value.split(delimiter)
    return []

@register.filter
def length(value):
    """
    Return the length of a list or string
    Usage: {{ value|length }}
    """
    try:
        return len(value)
    except:
        return 0

@register.filter
def get_type(value):
    """
    Return the type of a value
    Usage: {{ value|get_type }}
    """
    return type(value).__name__

@register.filter
def is_list(value):
    """
    Check if value is a list
    Usage: {{ value|is_list }}
    """
    return isinstance(value, (list, tuple))

@register.filter
def is_dict(value):
    """
    Check if value is a dictionary
    Usage: {{ value|is_dict }}
    """
    return isinstance(value, dict)

@register.filter
def multiply(value, arg):
    """
    Multiply the value by the argument
    Usage: {{ value|multiply:2 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """
    Divide the value by the argument
    Usage: {{ value|divide:2 }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def format_number(value):
    """
    Format number with commas
    Usage: {{ value|format_number }}
    """
    try:
        return "{:,}".format(float(value))
    except (ValueError, TypeError):
        return value

@register.filter
def strip_special_chars(value):
    """
    Remove special characters from string
    Usage: {{ value|strip_special_chars }}
    """
    if not isinstance(value, str):
        return value
    import re
    return re.sub(r'[^a-zA-Z0-9\s]', '', value)

@register.filter
def truncate_string(value, length=50):
    """
    Truncate string to specified length
    Usage: {{ value|truncate_string:50 }}
    """
    if not isinstance(value, str):
        return value
    if len(value) <= length:
        return value
    return value[:length] + '...'

@register.filter
def join_list(value, separator=', '):
    """
    Join list elements with a separator
    Usage: {{ list|join_list:", " }}
    """
    if isinstance(value, (list, tuple)):
        return separator.join(str(x) for x in value)
    return value

@register.filter
def bool_to_string(value):
    """
    Convert boolean to Yes/No
    Usage: {{ value|bool_to_string }}
    """
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return value

@register.filter
def get_list_item(lst, index):
    """
    Get item from list by index
    Usage: {{ list|get_list_item:0 }}
    """
    try:
        return lst[int(index)]
    except (IndexError, TypeError, ValueError):
        return None

@register.filter
def format_phone(value):
    """
    Format phone number
    Usage: {{ value|format_phone }}
    """
    if not value:
        return value
    try:
        value = str(value)
        if len(value) == 10:
            return f"{value[:3]}-{value[3:6]}-{value[6:]}"
        return value
    except:
        return value

@register.filter
def currency_format(value):
    """
    Format value as currency
    Usage: {{ value|currency_format }}
    """
    try:
        return "₹{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return value
