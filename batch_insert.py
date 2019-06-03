# -*- coding: utf-8 -*-
def batch_insert(cursor, sql_insert, sql_values, values, batch_size=10000):
    """
    sql批量插入
    >>> import sqlite3
    >>> con = sqlite3.connect(':memory:')
    >>> cur = con.cursor()
    >>> _ = cur.execute('CREATE TABLE `test` (`id` integer, `name` varchar(50))')
    >>> sql_insert = "INSERT INTO `test` (id, name) VALUES "
    >>> sql_values = "(%d, '%s')"
    >>> values = [(i, f'test{i}') for i in range(1, 5)]
    >>> batch_insert(cur, sql_insert, sql_values, values, 1)
    >>> _ = cur.execute('SELECT * FROM `test`')
    >>> cur.fetchall()
    [(1, 'test1'), (2, 'test2'), (3, 'test3'), (4, 'test4')]LF
    >>> _ = cur.execute('DELETE FROM `test`')
    >>> batch_insert(cur, sql_insert, sql_values, values, 2)
    >>> _ = cur.execute('SELECT * FROM `test`')
    >>> cur.fetchall()
    [(1, 'test1'), (2, 'test2'), (3, 'test3'), (4, 'test4')]
    >>> _ = cur.execute('DELETE FROM `test`')
    >>> batch_insert(cur, sql_insert, sql_values, values, 3)
    >>> _ = cur.execute('SELECT * FROM `test`')
    >>> cur.fetchall()
    [(1, 'test1'), (2, 'test2'), (3, 'test3'), (4, 'test4')]
    >>> _ = cur.execute('DELETE FROM `test`')
    >>> batch_insert(cur, sql_insert, sql_values, values, 4)
    >>> _ = cur.execute('SELECT * FROM `test`')
    >>> cur.fetchall()
    [(1, 'test1'), (2, 'test2'), (3, 'test3'), (4, 'test4')]
    >>> _ = cur.execute('DELETE FROM `test`')
    """
    tmp = []
    while len(values) > 0:
        tmp = values[:batch_size]
        values = values[batch_size:]
        sql = sql_insert + ', '.join([sql_values % value for value in tmp])
        cursor.execute(sql)
