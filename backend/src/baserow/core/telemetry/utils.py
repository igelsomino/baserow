import functools

from opentelemetry.context import attach, detach, set_value


def disable_instrumentation(wrapped_function):
    @functools.wraps(wrapped_function)
    def _wrapper(*args, **kwargs):
        token = attach(set_value("suppress_instrumentation", True))
        result = wrapped_function(*args, **kwargs)
        detach(token)
        return result

    return _wrapper
