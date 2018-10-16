import pymysql
from DBUtils.PooledDB import PooledDB
from collections import namedtuple


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
        MysqlManager.pool = PooledDB(creator=pymysql, maxconnections=max_overflow, host=host, port=port, user=user, passwd=passwd,
                                     db=db, charset=charset, cursorclass=pymysql.cursors.DictCursor)

    @staticmethod
    def execute(sql):
        conn = MysqlManager.pool.connection()
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

    @staticmethod
    def insert(table, **kwargs):
        keys = []
        values = []
        for key, value in kwargs.items():
            keys.append(key)
            values.append("'{0}'".format(value) if type(value) not in [int, float] else str(value))
        sql = "insert into {0}({1}) values({2})".format(table, ",".join(keys), ",".join(values))
        MysqlManager.execute(sql)


if __name__ == "__main__":
    mysqldb = MysqlManager(host="localhost")
    sql = "select * from student"
    result = MysqlManager.execute(sql)
    print(next(result).id)
