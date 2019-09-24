# coding=utf-8
"""
-------------------------------------------------
   File Name：     insert_sys_info_to_db
   Description :
   Author :       'li'
   date：          2019/9/11
-------------------------------------------------
   Change Activity:
                   2019/9/11:
-------------------------------------------------
"""
__author__ = 'li'
from common.utility.file_path_utility import combine_file_path
from common.utility.uuid_utility import get_uuid_str
from db_utility.db_pool import DB_POOL
from db_utility.sql_str import INSERT_SYS_INFO

import csv


def get_sys_infos():
    """
    get sys info
    :return:
    """
    file_name = combine_file_path('data_conversion/csv_to_db/fff.csv')
    all_items = set()
    with open(file_name, mode='r', encoding='utf8')as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if row[0] is None:
                continue
            all_items.add(row[0])
    return all_items


def insert_sys_infos(sys_infos):
    """
    insert sys info
    :param sys_infos:
    :return:
    """
    sqls = []
    for info in sys_infos:
        value = (get_uuid_str(), info)
        sql = INSERT_SYS_INFO % value
        sqls.append(sql)
    count = DB_POOL.execute_sql_array(sqls)
    print('execute sql :' + str(count))


def main():
    sys_infos = get_sys_infos()
    insert_sys_infos(sys_infos)
    pass


if __name__ == '__main__':
    main()
