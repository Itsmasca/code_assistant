# core/decorators/error_handling.py
from functools import wraps
import logging
from typing import Callable, Any
from src.api.core.logs.logger import Logger
import asyncio
import logging
from functools import wraps
from typing import Any, Callable

def service_error_handler(module: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(self, *args: Any, **kwargs: Any) -> Any:
                try:
                    return await func(self, *args, **kwargs)
                except Exception as e:
                    self._logger.log(
                        message=f"Error in {func.__name__}",
                        level=logging.ERROR,
                        name=f"{module}.{func.__name__}",
                        exc_info=True
                    )
                    raise
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(self, *args: Any, **kwargs: Any) -> Any:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    self._logger.log(
                        message=f"Error in {func.__name__}",
                        level=logging.ERROR,
                        name=f"{module}.{func.__name__}",
                        exc_info=True
                    )
                    raise
            return sync_wrapper
    return decorator
