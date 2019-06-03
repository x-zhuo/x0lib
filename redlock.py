"""
来自: https://github.com/rfyiamcool/redis_netlock
>>> import time
>>> import redlock
>>> with redlock.dist_lock('my-lock'):
...    t0 = time.time()
...    time.sleep(10)
"""
import time
from contextlib import contextmanager

import redis

DEFAULT_EXPIRES = 30


@contextmanager
def dist_lock(name, **redis_kw):
    key = 'redlock:%s' % name
    client = redis.StrictRedis(**redis_kw)
    try:
        b = _acquire_lock(key, client)
        yield b
    finally:
        _release_lock(key, client)


def _acquire_lock(key, client):
    while 1:
        get_stored = client.get(key)
        if get_stored:
            time.sleep(0.03)
        else:
            if client.set(key, 1, ex=DEFAULT_EXPIRES, nx=True):
                return True
    return False


def _release_lock(key, client):
    client.delete(key)
