import pymysql
from DBUtils.PooledDB import PooledDB

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
                 cursorclass=pymysql.cursors.DictCursor):
        MysqlManager.pool = PooledDB(creator=pymysql, maxconnections=10, host=host, port=port, user=user, passwd=passwd,
                                db=db, charset=charset, cursorclass=cursorclass)

    @staticmethod
    def execute(sql):
        conn = MysqlManager.pool.connection()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            dbout =cur.fetchall()
            conn.commit()
            res = True
        except Exception as e:
            print("sql:{0},执行错误:{1}".format(sql, str(e)))
            conn.rollback()
            res = False
            dbout = None
        finally:
            conn.close()
            cur.close()
        return res, dbout

if __name__ == "__main__":
    mysqldb = MysqlManager(host="localhost")
    sql = "select * from student"
    res, dbout = MysqlManager.execute(sql)
    print([r for r in dbout])