import pymysql
import threading
import traceback
import sys

config = {
    "host" : "localhost",
    "port" : 3306,
    "user" : "root",
    "passwd" : "123456",
    "db" : "mysql",
    "charset" : "utf8",
    "cursorclass" : pymysql.cursors.DictCursor
}

class DBConfig:
    def __init__(self, host="localhost", port=3306, user="root",
                 passwd="123456", db="mysql", charset="utf8", cursorclass=pymysql.cursors.DictCursor):
        self.host = host
        self.port = 3306
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.cursorclass = cursorclass

    def getdict(self):
        return self.__dict__

class Singleton(object):
    _instance = None
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if Singleton._instance is None:
            Singleton._instance = object.__new__(cls, *args, **kwargs)
        return Singleton._instance

class mysqlDB(Singleton):
    connection = None
    cursor = None
    lock = threading.Lock()
    def __init__(self):
       pass

    @staticmethod
    def connectDB(config):
        mysqlDB.connection = pymysql.connect(**config)
        mysqlDB.cursor = mysqlDB.connection.cursor()

    @staticmethod
    def execute(sql):
        try:
            with mysqlDB.lock:
                mysqlDB.cursor.execute(sql)
                result = mysqlDB.cursor.fetchall()
                mysqlDB.connection.commit()
                bRes = True
        except Exception as e:
            traceback.print_exc()
            #print sys.exc_info()
            mysqlDB.connection.rollback()
            bRes = False
            result = None
        return bRes, result

if __name__ == "__main__":
    dbConfig = DBConfig().getdict()
    mysqlDB.connectDB(dbConfig)
    sql = "select * from student"
    bRes, result = mysqlDB.execute(sql)
    print([r for r in result])