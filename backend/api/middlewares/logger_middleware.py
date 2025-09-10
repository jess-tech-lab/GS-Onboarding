from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import json
import time
from datetime import datetime
from backend.utils.logging import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided. 
        Logs should be printed so that they are easily readable and understandable. 

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method
        start_time = time.time()
        request_time = datetime.now().isoformat()

        # Read if valid body for non-GET requests
        try:
            body_bytes = await request.body()
            if body_bytes:
                try:
                    body = json.loads(body_bytes.decode("utf-8"))
                except json.JSONDecodeError:
                    body = body_bytes.decode("utf-8")
            else:
                body = None
        except Exception:
            body = "<unable to read body>"
        
        logger.info(f"Request received at {request_time} for {request.url.path} with params {request.query_params} and body { body }")

        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"Response sent for {request.url.path} with status code {response.status_code} in {duration:.4f} seconds")

        return response
    