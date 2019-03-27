import collections

from datetime import datetime


def get_timestamp():
    return datetime.now()


def reversed_order_dict(regular_dict):
    ordered_dict = collections.OrderedDict(sorted(regular_dict.items(), reverse=True))
    return ordered_dict
