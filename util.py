import time
import collections


def get_timestamp():
    return int(time.time())


def reversed_order_dict(regular_dict):
    ordered_dict = collections.OrderedDict(sorted(regular_dict.items(), reverse=True))
    return ordered_dict
