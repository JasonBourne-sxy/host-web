# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     db_util_pool
   Description :
   Author :       'li'
   date：          2019/9/20
-------------------------------------------------
   Change Activity:
                   2019/9/20:
-------------------------------------------------
"""
import pymysql

from config import *

__author__ = 'li'
from DBUtils.PooledDB import PooledDB


class MySQL_Util_Pool:

    def __init__(self):
        self.pool = PooledDB(pymysql, 3, host=DB_IP, user=DB_USER, passwd=DB_PASSWORD,
                             db=DB_NAME,
                             port=DB_PORT, charset='utf8',
                             use_unicode=True, maxcached=50)

    def select(self, sql):
        """

        :param sql:
        :return:
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        columns = cursor._cursor.description
        return_result = []
        for item in result:
            obj = {}
            for index, column in enumerate(columns):
                key = column[0]
                value = item[index]
                obj[key] = value
            return_result.append(obj)
        cursor.close()
        conn.close()
        return return_result

    def get_count(self, sql):
        """

        :param sql:
        :return:
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return len(result)

    def execute_sql_str(self, sql):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            print(sql)
            conn.rollback()
            return {'result': False, 'err': err}
        finally:
            cursor.close()
            conn.close()

    def execute_sql_array(self, sqls):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            for sql in sqls:
                cursor.execute(sql)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            print(err)
            conn.rollback()
            return {'result': False, 'err': err}
        finally:
            cursor.close()
            conn.close()


DB_POOL = MySQL_Util_Pool()


def main():
    sql = """INSERT INTO `log` (`id`,`log_level`,`time`,`name`,`description`) VALUES ('c3f2512ffc4104ae4d5cd054d719ad','info','2019-09-20 11:53:38','launch','launch sniff,local ip %(172)s.21.12.230');"""
    res = DB_POOL.execute(sql)
    sql = """select * from log"""
    DB_POOL.select(sql)
    print(res)


if __name__ == '__main__':
    main()
