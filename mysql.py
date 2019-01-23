import pymysql
from DBUtils.PooledDB import PooledDB
from collections import namedtuple
from datetime import datetime


# class Singleton(object):
#     _instance = None
#
#     def __init__(self):
#         pass
#
#     def __new__(cls, *args, **kwargs):
#         if Singleton._instance is None:
#             Singleton._instance = super(Singleton, cls).__new__(cls)
#         return Singleton._instance


class SingletonMeta(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance


class PoolConnection:
    def __init__(self, pool):
        self.connect = pool.connection()
        self.cursor = self.connect.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connect.close()


class MysqlManager(metaclass=SingletonMeta):
    def __init__(self, host="localhost", port=3306, user="root", password="123456", db="mysql", charset="utf8",
                 max_overflow=10):
        self._pool = PooledDB(creator=pymysql, maxconnections=max_overflow, host=host, port=port, user=user,
                              password=password,
                              db=db, charset=charset, cursorclass=pymysql.cursors.DictCursor)

    def execute(self, sql, args=None):
        with PoolConnection(pool=self._pool) as p:
            try:
                p.cursor.execute(sql, args)
                records = p.cursor.fetchall()
                if records:
                    fields = [filed[0] for filed in p.cursor.description]
                    Record = namedtuple("Record", fields)
                    for record in records:
                        yield Record(**record)
            except Exception as e:
                p.connect.rollback()
                raise RuntimeError("[sql:{}, args:{}]语句执行出错:{}".format(sql, args, e))

    def insert(self, table, **kwargs):
        sql = "insert into {table}({keys}) values({values})".format(table=table, keys=",".join(kwargs.keys()),
                                                                    values=",".join(
                                                                        ["%s" for i in range(len(kwargs.values()))]))

        rows = 0
        with PoolConnection(pool=self._pool) as p:
            try:
                rows = p.cursor.execute(sql, tuple(kwargs.values()))
                p.connect.commit()
            except Exception as e:
                p.connect.rollback()
                raise RuntimeError("[sql:{}, args:{}]语句执行出错:{}".format(sql, tuple(kwargs.values()), e))
        return rows

    def select(self, table, conditions=None, order_by=None, limit=None):
        sql = "select * from {table}".format(table=table)

        if conditions:
            sql = "{query} where {conditions}".format(query=sql, conditions=conditions)

        if order_by:
            order_by = order_by if order_by[0] != "-" else "{0} desc".format(order_by[1:])
            sql = "{query} order by {order_by}".format(query=sql, order_by=order_by)

        if limit:
            sql = "{query} limit {num}".format(query=sql, num=limit)

        return self.execute(sql)

    def count(self, table, conditions=None):
        sql = "select count(1) as nums from {table}".format(table=table)
        if conditions:
            sql = "{query} where {conditions}".format(query=sql, conditions=conditions)
        result = self.execute(sql)
        for r in result:
            return r.nums
        return 0

    def exist(self, table, conditions):
        sql = "select 1 as is_exist from {table} where {conditions} limit 1".format(table=table, conditions=conditions)
        result = list(self.execute(sql))
        if result:
            return True
        else:
            return False


if __name__ == "__main__":
    mysqldb = MysqlManager(host="localhost")
    # print(mysqldb.exist("student", conditions="name='ouru'"))

    # mysqldb.insert("student", name="ouru", age=30, add_time=datetime.now())

    rescords = mysqldb.execute("select * from student where name=%s and age=%s", args=("ouru", 22, 23))
    # rescords = mysqldb.execute("select * from student where name='ouru'")
    print(list(rescords))
