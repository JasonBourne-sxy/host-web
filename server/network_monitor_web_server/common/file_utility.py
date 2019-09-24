import os
import shutil


def create_dir(dir_path):
    """
    create dir
    :param dir_path:
    :return:
    """
    is_exist = os.path.exists(dir_path)
    if not is_exist:
        os.makedirs(dir_path)


"""
利用递归实现目录的遍历
@para  sourcePath:原文件目录
@para  targetPath:目标文件目录
"""


def copy_dir(sourcePath, targetPath):
    if not os.path.exists(sourcePath):
        return
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    # 遍历文件夹
    for fileName in os.listdir(sourcePath):
        # 拼接原文件或者文件夹的绝对路径
        absourcePath = os.path.join(sourcePath, fileName)
        # 拼接目标文件或者文件加的绝对路径
        abstargetPath = os.path.join(targetPath, fileName)
        # 判断原文件的绝对路径是目录还是文件
        if os.path.isdir(absourcePath):
            # 是目录就创建相应的目标目录
            create_dir(abstargetPath)
            # 递归调用getDirAndCopyFile()函数
            copy_dir(absourcePath, abstargetPath)
        # 是文件就进行复制
        if os.path.isfile(absourcePath):
            shutil.copy(absourcePath, abstargetPath)
