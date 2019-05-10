import pytest

from django.db import OperationalError
from django.http import HttpRequest
from django.conf import settings

from deadlock_middleware import DeadlockRetryMiddleware


def get_response(request):
    return request

middleware = DeadlockRetryMiddleware(get_response)


def test_call_adds_retry_count():
    request = HttpRequest()

    result = middleware(request)

    assert result.deadlock_retry_attempt == 1


def test_process_view_disables_if_non_atomic_requests_set():
    def view_func(request, *args, **kwargs):
        return request

    view_func._non_atomic_requests = {1}

    request = HttpRequest()

    middleware.process_view(request, view_func, [], {})

    assert request.disable_deadlock_retry == True


def test_process_view_enables_if_non_atomic_requests_not_set():
    def view_func(request, *args, **kwargs):
        return request

    view_func._non_atomic_requests = set()

    request = HttpRequest()

    middleware.process_view(request, view_func, [], {})

    assert request.disable_deadlock_retry == False


def test_process_exception_increments_deadlock_retry_count_on_deadlock():
    request = HttpRequest()
    request.disable_deadlock_retry = False
    request.deadlock_retry_attempt = 1

    exception = OperationalError('deadlock detected')

    result = middleware.process_exception(request, exception)

    assert result.deadlock_retry_attempt > 1


def test_process_exception_returns_none_if_attempts_exceeded():
    request = HttpRequest()
    request.disable_deadlock_retry = False
    request.deadlock_retry_attempt = 11

    settings.DEADLOCK_RETRY_ATTEMPTS = 10

    exception = OperationalError('deadlock detected')

    result = middleware.process_exception(request, exception)

    assert result is None


def test_process_exception_returns_none_if_not_operational_error():
    request = HttpRequest()
    request.disable_deadlock_retry = False
    request.deadlock_retry_attempt = 1

    exception = Exception('not a deadlock')

    result = middleware.process_exception(request, exception)

    assert result is None


def test_process_exception_returns_none_if_not_deadlock_error():
    request = HttpRequest()
    request.disable_deadlock_retry = False
    request.deadlock_retry_attempt = 1

    exception = OperationalError('not a deadlock')

    result = middleware.process_exception(request, exception)

    assert result is None


def test_process_exception_returns_none_if_retry_disabled():
    request = HttpRequest()
    request.disable_deadlock_retry = True
    request.deadlock_retry_attempt = 1

    exception = OperationalError('deadlock detected')

    result = middleware.process_exception(request, exception)

    assert result is None
