# Copyright 2018 eShares, Inc. dba Carta, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

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
