import atexit
import functools
import time
from enum import Enum as _Enum

_PROFILE_STATS = {}


def timer(func):
    @functools.wraps(func)
    def _timer(*w_args, **w_kwargs):
        start_time = time.monotonic()
        try:
            result = func(*w_args, **w_kwargs)
        finally:
            end_time = time.monotonic()
            time_taken = end_time - start_time
            _PROFILE_STATS.setdefault(func.__name__, []).append(time_taken)

        return result

    return _timer


def print_stats():
    for func, data in _PROFILE_STATS.items():
        total_runtime = sum(data)
        call_count = len(data)
        average = total_runtime / call_count
        print(f"Stats for method: {func!r}")
        print(f"  call count:       {call_count}")
        print(f"  total run time:   {total_runtime}")
        print(f"  average run time: {average}")


atexit.register(print_stats)


class Enum(_Enum):
    @classmethod
    def values(cls):
        """Values of this enum"""
        if not hasattr(cls, "__values__"):
            setattr(cls, "__values__", set(i.value for i in cls))
        return getattr(cls, "__values__")

    @classmethod
    def contains(cls, value):
        """Returns whether the Enum contains the given value"""
        return value in cls.values()
