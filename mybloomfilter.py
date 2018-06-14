# -*- coding: utf-8 -*-
import hashlib

"""
布隆过滤器简单实现
实际应用的难点在于hash函数的选择(算法和个数)以及保证误报率
***************************************************************
http://www.cnblogs.com/allensun/archive/2011/02/16/1956532.html
hash函数的个数 k=0.6185*m/n 时误报率最低(m: 数组长度, n: 元素个数)
---------------------------------------------------------------
@datetime: 2018/6/14 15:33
"""


class MyBloomFilter:
    def __init__(self, size):
        # 选取一些值生成不同hash函数
        self.__seeds = [2, 3, 5, 7, 11, 13, 17, 19]
        self.size = size
        self.bf = [False]*size

    def add(self, text):
        for p in self.make_hashs(text):
            # 将hash函数对应位置赋值为True
            self.bf[p] = True

    def __contains__(self, text):
        # 判断是否所有hash函数都落在数组上，如果都落在数组上即该元素很可能在集合中。如不全落在数组上，那么该元素一定不在集合中
        return all([self.bf[p] for p in self.make_hashs(text)])

    def make_hashs(self, text):
        # int(hashlib.md5((str(seed)+text).encode('utf-8')).hexdigest(), 16) % self.size
        # 拼接seed和待处理字符串，获取其md5值并转换为10进制整型，用数组长度取余数，即获得该hash函数在数组上对应的位置
        # !! md5的离散程度好像不够高，可以换用其他hash算法
        return [int(hashlib.md5((str(seed)+text).encode('utf-8')).hexdigest(), 16) % self.size for seed in self.__seeds]


def test(size=1000):
    import random
    import string
    bf = MyBloomFilter(10000)
    # 随机生成长度为10的由大写和小写字母及数字组成的字符串
    test_strs = [''.join(random.choices(
        string.ascii_letters+string.digits, k=10)) for _ in range(size)]

    # 添加所有字符串到过滤器中
    for s in test_strs:
        bf.add(s)

    # 根据这个算法，原始集合中的数据必须能匹配到
    for s in test_strs:
        assert s in bf

    # 这个如果匹配到了就属于误报
    assert 'xuzhuo' not in bf

    print('test pass.')


if __name__ == '__main__':
    test(1000)
