"""
基于redis的队列
原文:http://peter-hoffmann.com/2012/python-simple-queue-redis-queue.html
再原作者的基础上增加使用了json进行序列化,尽量接近官方queue模块

from redque import RedisQueue
q = RedisQueue('my-queue')
q.put(1)
q.get()
"""
import json
import pickle

import redis


class RedisQueue(object):
    def __init__(self, name, namespace="redque", serialized="json", **redis_kw):
        """
        支持 pickle 和 json 两种序列化方式, 已知json不支持 datetime 类型
        :param name:
        :param namespace:
        :param serialized:  "json" or "pickle"
        :param redis_kw:
        """
        self.__db = redis.StrictRedis(**redis_kw)
        self.key = "%s:%s" % (namespace, name)
        if serialized == "json":
            self.serialized = json
        elif serialized == "pickle":
            self.serialized = pickle
        else:
            raise NameError

    def qsize(self):
        """
        返回队列长度
        """
        return self.__db.llen(self.key)

    def empty(self):
        """
        返回队列是否为空
        """
        return self.qsize() == 0

    def put(self, item):
        """
        放数据进队列
        """
        serialized_item = self.serialized.dumps(item)
        return self.__db.rpush(self.key, serialized_item)

    def get(self, block=True, timeout=None):
        """从队列取出数据
        """
        if block:  # 阻塞模式
            serialized_item = self.__db.blpop(self.key, timeout=timeout)
            # blpop返回的是一个(key,value)的tuple,只需要获取value
            if serialized_item:
                serialized_item = serialized_item[1]
        else:  # 非阻塞模式,serialized_item可以为空
            serialized_item = self.__db.lpop(self.key)

        if serialized_item:
            if self.serialized == json:
                # FIX python3.6之前版本json.loads()不支持bytes (2017/09/05)
                item = self.serialized.loads(serialized_item.decode())
            else:
                item = self.serialized.loads(serialized_item)
        else:
            raise EmptyError
        return item

    def get_nowait(self):
        return self.get(False)

    # TODO: 增加锁


class EmptyError(Exception):
    pass
