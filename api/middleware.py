"""
Middleware to log all requests and responses.
Uses a logger configured by the name of django.request
to log all requests and responses according to configuration
specified for django.request.
"""
import logging
import math
import socket
import time

from django.utils.deprecation import MiddlewareMixin

request_logger = logging.getLogger('apiLogger')


class RequestLogMiddleware(MiddlewareMixin):
    """Request Logging Middleware."""

    def __init__(self, *args, **kwargs):
        """Constructor method."""
        super().__init__(*args, **kwargs)

    def process_request(self, request):
        """Set Request Start Time to measure time taken to service request."""
        request.start_time = time.time()

    def extract_log_info(self, request):
        """Extract appropriate log info from requests/responses/exceptions."""
        log_data = {
            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'request_method': request.method,
            'request_path': request.get_full_path(),
            'run_time': math.floor((time.time() - request.start_time) * 1000),
        }
        return log_data

    def process_response(self, request, response):
        """Log data using logger."""
        log_data = self.extract_log_info(request)
        msg = '{} {} {} {}ms'.format(
            log_data.get('request_method'),
            log_data.get('request_path'),
            response.status_code,
            log_data.get('run_time'),
        )
        request_logger.info(msg=msg)
        return response

    def process_exception(self, request, exception):
        """Log Exceptions."""
        try:
            raise exception
        except Exception:
            request_logger.exception(msg="Unhandled Exception")
        return exception
