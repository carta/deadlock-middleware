import logging

from django.conf import settings
from django.db import OperationalError
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class DeadlockRetryMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        non_atomic_requests = getattr(view_func, "_non_atomic_requests", set())

        if non_atomic_requests:
            return view_func(request, *view_args, **view_kwargs)

        attempt = 0

        retry_attempts = getattr(settings, "DEADLOCK_RETRY_ATTEMPTS", 2)

        while attempt < retry_attempts:
            try:
                return view_func(request, *view_args, **view_kwargs)
            except OperationalError as e:
                is_deadlock = e.args[0].startswith("deadlock detected")

                if not is_deadlock:
                    raise e

                attempt += 1
                logger.warning("deadlock detected - retrying request")

        return view_func(request, *view_args, **view_kwargs)
