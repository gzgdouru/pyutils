import pymysql
from DBUtils.PooledDB import PooledDB
from collections import namedtuple


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

    def execute(self, sql):
        with PoolConnection(pool=self._pool) as p:
            try:
                row_num = p.cursor.execute(sql)
                p.connect.commit()
                records = p.cursor.fetchall()
                if records:
                    fields = [filed[0] for filed in p.cursor.description]
                    Record = namedtuple("Record", fields)
                    for record in records:
                        yield Record(**record)
            except Exception as e:
                p.connect.rollback()
                raise RuntimeError("sql[{0}]执行出错:{1}".format(sql, str(e)))

    def insert(self, table, **kwargs):
        keys = []
        values = []
        for key, value in kwargs.items():
            keys.append(key)
            values.append("'{0}'".format(value) if type(value) not in [int, float] else str(value))
        sql = "insert into {0}({1}) values({2})".format(table, ",".join(keys), ",".join(values))

        rows = 0
        with PoolConnection(self.pool) as p:
            try:
                rows = p.cursor.execute(sql)
                p.connect.commit()
            except Exception as e:
                p.connect.rollback()
                raise RuntimeError("sql[{0}]执行出错:{1}".format(sql, str(e)))
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
    # rescords = mysqldb.execute("insert into student(name, age, add_time) values('ouru', 28, now())")
    rescords = mysqldb.execute("select * from student")
    print(list(rescords))
    print('-' * 100)
    mysqldb = MysqlManager(host="localhost", db="django_test")
    rescords = mysqldb.execute("select * from student")
    print(list(rescords))
