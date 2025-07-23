import asyncio
import logging
from functools import wraps
from typing import Any, Callable


def log_exceptions(module: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        is_async = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logging.error(
                    f"[{module}.{func.__name__}] Exception: {e}",
                    exc_info=True
                )
                raise

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(
                    f"[{module}.{func.__name__}] Exception: {e}",
                    exc_info=True
                )
                raise

        return async_wrapper if is_async else sync_wrapper

    return decorator
