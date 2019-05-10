import logging

from django.conf import settings
from django.db import OperationalError

logger = logging.getLogger(__name__)


class DeadlockRetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.deadlock_retry_attempt = 1

        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        non_atomic_requests = getattr(view_func, "_non_atomic_requests", set())

        request.disable_deadlock_retry = bool(non_atomic_requests)

    def process_exception(self, request, exception):
        if request.disable_deadlock_retry:
            return None

        if not isinstance(exception, OperationalError):
            return None

        if not exception.args[0].startswith("deadlock detected"):
            return None

        total_retry_attempts = getattr(settings, "DEADLOCK_RETRY_ATTEMPTS", 2)
        if request.deadlock_retry_attempt < total_retry_attempts:
            logger.warning("deadlock detected at {} - retrying".format(request.path))

            request.deadlock_retry_attempt += 1

            return self.get_response(request)
