from django.utils.deprecation import MiddlewareMixin
from .services import log_visit

class LogVisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        log_visit(request)