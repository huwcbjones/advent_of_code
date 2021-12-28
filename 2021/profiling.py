"""Function timing decorators"""
import atexit
import dataclasses
import functools
import inspect
import logging
import statistics
import time
from collections import deque, defaultdict
from typing import Dict, Deque


LOGGER = logging.getLogger(__name__)

_FUNCTIONS_TO_IGNORE = {
    "_wrapper",
    "wrapper",
    "timer",
    "_timer",
    "__timer",
    "log_duration",
}
_DEFAULT_LOGGING_LEVEL = logging.DEBUG
_DEFAULT_ANALYSE_CALLS = False


@dataclasses.dataclass
class CallMetric:
    func_name: str
    """Function name"""
    samples: int
    """Number of call samples"""
    duration: float
    """Total duration of all calls (in set of samples) / s"""
    min: float
    """Minimum call duration / ms"""
    max: float
    """Maximum call duration / ms"""
    avg: float
    """Average (mean) call duration / ms"""
    stddev: float
    """StdDev of call durations / ms"""


class _ProfileMetrics:
    def __init__(self):
        self._metrics: Dict[str, Deque[float]] = defaultdict(
            lambda: deque(maxlen=50000)
        )
        atexit.register(self.dump_call_metrics)

    def add_call(self, func_name: str, value: float):
        self._metrics[func_name].append(value)

    def get_metrics(self, func_name: str) -> CallMetric:
        call_data = self._metrics[func_name]
        if not call_data:
            return CallMetric(func_name, 0, 0, 0, 0, 0, 0)
        mean = statistics.mean(call_data)
        return CallMetric(
            func_name,
            len(call_data),
            sum(call_data) / 1000,
            min(call_data),
            max(call_data),
            mean,
            statistics.stdev(call_data, mean),
        )

    def dump_call_metrics(self, func_name: str = None):
        if func_name:
            funcs = [func_name]
        else:
            funcs = list(self._metrics)

        if not funcs:
            return

        metric_report = """
## FUNCTION CALL REPORT
    min,     avg,     max, stddev, samples, total (s), function
"""
        for func_name in funcs:
            metric = self.get_metrics(func_name)
            metric_report += "{:> 7.3f}, {:> 7.3f}, {:> 7.3f}, {:> 7.3f}, {:> 6}, {:> 9.3f}, {}\n".format(
                metric.min,
                metric.avg,
                metric.max,
                metric.stddev,
                metric.samples,
                metric.duration,
                metric.func_name,
            )
        LOGGER.info(metric_report)


_CALL_METRICS = _ProfileMetrics()


def log_duration(func, time_taken: float, level: int):
    """log duration function took to execute"""
    stack = inspect.stack()
    frame = stack[0]
    count = 0
    while frame.function in _FUNCTIONS_TO_IGNORE:
        count = count + 1
        frame = stack[count]
    LOGGER.log(
        level,
        "%s took %.5fs (called from %s)",
        func.__qualname__,
        time_taken,
        frame.function,
    )


def profile(*args):
    """
    Profiler Decorator
    Wraps a function in timing code, default logger.level is INFO.
    :param args: logger.level
    :return:
    """

    def _timer(func):
        assert inspect.isfunction(func) or inspect.ismethod(
            func
        ), f"{func} is not a valid function"

        func_name = func.__qualname__

        @functools.wraps(func)
        def __timer(*w_args, **w_kwargs):
            # If we're not going to log the time taken, don't bother profiling
            should_log_duration = LOGGER.isEnabledFor(level)
            if not should_log_duration and not analyse_calls:
                return func(*w_args, **w_kwargs)

            start_time = time.perf_counter_ns()
            try:
                result = func(*w_args, **w_kwargs)
            finally:
                time_taken = (time.perf_counter_ns() - start_time) / 1_000_000
                if analyse_calls:
                    _CALL_METRICS.add_call(func_name, time_taken)
                if should_log_duration:
                    log_duration(func, time_taken / 1000, level)
            return result

        return __timer

    # If we only have 1 arg and it's callable, then we know it's the decorated function
    level = _DEFAULT_LOGGING_LEVEL
    analyse_calls = _DEFAULT_ANALYSE_CALLS
    if len(args) == 1 and callable(args[0]):
        return _timer(args[0])

    if len(args) >= 2:
        level, analyse_calls, _ = args
    elif isinstance(args[0], bool):
        analyse_calls = args[0]
    elif isinstance(args[0], int):
        level = args[0]

    return _timer
