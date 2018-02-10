import pytest
from redque import RedisQueue
from datetime import datetime


class TestRedisQueue:

    # scope = "function" 会在每次方法运行周期执行
    @pytest.fixture(scope="function")
    def que(self):
        # 返回一个队列，并在使用后清除该队列
        q = RedisQueue('tests')
        # 此处返回的即为que的值
        yield q
        # yield 前面属于setUp部分，后面属于tearDown
        import redis
        r = redis.Redis()
        r.delete(q.key)

    def test_qsize_and_empty(self, que):
        q = que
        assert q.qsize() == 0
        assert q.empty()
        q.put(1)
        assert q.qsize() == 1

    @pytest.mark.parametrize('data', [123, 1.23, True, "abc", [1, 2, 3], {"a": 1, "b": False}])
    def test_put_get_json(self, que, data):
        q = que
        q.put(data)
        assert q.get() == data

    @pytest.mark.parametrize('data', [123, 1.23, datetime.now(), True, "abc", [1, 2, 3], {"a": 1, "b": False}])
    def test_put_get_pickle(self, que, data):
        import pickle
        q = que
        q.serialized = pickle
        q.put(data)
        assert q.get() == data
