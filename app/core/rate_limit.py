from time import time

# Separate stores
ip_store = {}
user_store = {}
token_store = {}

MAX_REQUESTS = 20
WINDOW_SECONDS = 60


def _cleanup(store, key):
    now = time()
    store[key] = [t for t in store.get(key, []) if now - t < WINDOW_SECONDS]


def check_limit(store, key):
    now = time()

    if key not in store:
        store[key] = []

    _cleanup(store, key)

    if len(store[key]) >= MAX_REQUESTS:
        return False

    store[key].append(now)
    return True


def is_allowed(ip: str, user: str = None, token: str = None):

    # IP level
    if not check_limit(ip_store, ip):
        return False, "IP rate limit exceeded"

    # User level
    if user:
        if not check_limit(user_store, user):
            return False, "User rate limit exceeded"

    # Token level
    if token:
        if not check_limit(token_store, token):
            return False, "Token rate limit exceeded"

    return True, None