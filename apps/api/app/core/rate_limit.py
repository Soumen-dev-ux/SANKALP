try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address

    limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])
except ImportError:
    class DummyLimiter:
        def limit(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator

    limiter = DummyLimiter()
    _rate_limit_exceeded_handler = None

