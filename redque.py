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

import redis


class RedisQueue(object):
    def __init__(self, name, namespace="redque", **redis_kw):
        self.__db = redis.StrictRedis(**redis_kw)
        self.key = "%s:%s" % (namespace, name)

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
        json_item = json.dumps(item)
        return self.__db.rpush(self.key, json_item)

    def get(self, block=True, timeout=None):
        """从队列取出数据
        """
        if block:  # 阻塞模式
            json_item = self.__db.blpop(self.key, timeout=timeout)
            # blpop返回的是一个(key,value)的tuple,只需要获取value
            if json_item:
                json_item = json_item[1]
        else:  # 非阻塞模式,json_item可以为空
            json_item = self.__db.lpop(self.key)

        if json_item:
            # FIX python3.6之前版本json.loads()不支持bytes (2017/09/05)
            item = json.loads(json_item.decode())
        else:
            raise EmptyError
        return item

    def get_nowait(self):
        return self.get(False)

    #TODO: 增加锁


class EmptyError(Exception):
    pass
