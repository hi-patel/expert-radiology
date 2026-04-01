from __future__ import annotations

from typing import Iterable

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class SimpleCorsMiddleware(MiddlewareMixin):
    """
    Very small CORS middleware to support the Next.js dev server on localhost:3000.

    This is only intended for local development; the production-like stack
    (served via nginx on port 8080) is same-origin and does not rely on CORS.
    """

    allowed_origins: Iterable[str] = ("http://localhost:3000",)

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        origin = request.META.get("HTTP_ORIGIN")
        if origin and origin in self.allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            request_headers = request.headers.get("Access-Control-Request-Headers")
            if request_headers:
                response["Access-Control-Allow-Headers"] = request_headers
            else:
                response["Access-Control-Allow-Headers"] = "Content-Type"

        if request.method == "OPTIONS":
            # Ensure a successful preflight for allowed origins.
            response.status_code = response.status_code or 200

        return response

