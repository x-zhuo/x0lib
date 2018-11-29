from mybloomfilter import MyBloomFilter


def test_mybloomfilter(size=1000):
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
