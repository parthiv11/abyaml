import time
import logging

logging.basicConfig(level=logging.INFO)

def retry_request(func):
    """Retry decorator for synchronous API requests."""
    def wrapper(*args, **kwargs):
        retries = 3
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < retries - 1:
                    logging.warning(f"Retrying due to: {e}")
                    time.sleep(2 ** attempt)
                else:
                    raise
    return wrapper
