import pymysql
from DBUtils.PooledDB import PooledDB
from collections import namedtuple
from datetime import datetime


class Singleton(object):
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if Singleton._instance is None:
            Singleton._instance = super(Singleton, cls).__new__(cls)
        return Singleton._instance


class MysqlManager(Singleton):
    pool = None

    def __init__(self, host="localhost", port=3306, user="root", passwd="123456", db="mysql", charset="utf8",
                 max_overflow=10):
        MysqlManager.pool = PooledDB(creator=pymysql, maxconnections=max_overflow, host=host, port=port, user=user,
                                     passwd=passwd,
                                     db=db, charset=charset, cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def execute(cls, sql):
        conn = cls.pool.connection()
        cur = conn.cursor()

        try:
            cur.execute(sql)
            conn.commit()
            fields = [filed[0] for filed in cur.description]
            Record = namedtuple("Record", fields)
            for record in cur.fetchall():
                yield Record(**record)
        except Exception as e:
            conn.rollback()
            raise RuntimeError("sql[{0}]执行出错:{1}".format(sql, str(e)))
        finally:
            conn.close()
            cur.close()

    @classmethod
    def insert(cls, table, **kwargs):
        keys = []
        values = []
        for key, value in kwargs.items():
            keys.append(key)
            values.append("'{0}'".format(value) if type(value) not in [int, float] else str(value))
        sql = "insert into {0}({1}) values({2})".format(table, ",".join(keys), ",".join(values))

        conn = cls.pool.connection()
        cur = conn.cursor()
        rows = 0

        try:
            rows = cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError("sql[{0}]执行出错:{1}".format(sql, str(e)))
        finally:
            conn.close()
            cur.close()
        return rows

    @classmethod
    def select(cls, table, conditions=None, order_by=None):
        sql = "select * from {table}".format(table=table)

        if conditions:
            sql = "{query} where {conditions}".format(query=sql, conditions=conditions)

        if order_by:
            order_by = order_by if order_by[0] != "-" else "{0} desc".format(order_by[1:])
            sql = "{query} order by {order_by}".format(query=sql, order_by=order_by)

        return cls.execute(sql)

    @classmethod
    def count(cls, table, conditions=None):
        sql = "select count(1) as nums from {table}".format(table=table)
        if conditions:
            sql = "{query} where {conditions}".format(query=sql, conditions=conditions)
        result = cls.execute(sql)
        for r in result:
            return r.nums
        return 0

    @classmethod
    def exist(cls, table, conditions):
        sql = "select 1 as is_exist from {table} where {conditions} limit 1".format(table=table, conditions=conditions)
        result = cls.execute(sql)
        for r in result:
            return True
        return False


if __name__ == "__main__":
    mysqldb = MysqlManager(host="localhost")
    rows = mysqldb.select("student")
    for row in rows:
        print(row)