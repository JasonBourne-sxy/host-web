# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     gen_obj_mapping
   Description :
   Author :       'li'
   date：          2019/9/11
-------------------------------------------------
   Change Activity:
                   2019/9/11:
-------------------------------------------------
"""
from common.utility.file_path_utility import combine_file_path
from db_utility.db_pool import DB_POOL
from db_utility.db_str.sql_str import GET_COLUMN_INFO

__author__ = 'li'


def gen_py_file(content):
    """
    gen py file
    :param content:
    :return:
    """
    for table_name in content:
        file_str = """class %s(object):
    def __init__(self):\n""" % table_name.upper()
        columns = content[table_name]
        for column in columns:
            line = """        self.%s = None\n""" % column
            file_str = file_str + line
        file_path = combine_file_path('object_mapping/' + str(table_name) + '.py')
        with open(file_path, mode='w', encoding='utf8') as file:
            file.write(file_str)


def gen_obj_mapping():
    """
    get obj mapping
    :return:
    """
    column_info = DB_POOL.get_all(GET_COLUMN_INFO)
    content = {}
    for info in column_info:
        table_name = info['TABLE_NAME']
        column_name = info['COLUMN_NAME']
        if table_name not in content.keys():
            content[table_name] = [column_name]
        else:
            content[table_name].append(column_name)
    gen_py_file(content)


if __name__ == '__main__':
    gen_obj_mapping()
