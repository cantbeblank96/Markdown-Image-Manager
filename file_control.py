import json
import os
import re
import time as t


# file name
def get_file_name(file_name, suffix='json', dtime=True):
    "return path: folder//NAME(__dtime__date).suffix"

    if dtime:
        stamp = t.time()
        date = t.strftime("%Y-%m-%d,%H;%M;%S", t.localtime(stamp))
        file_name = '__'.join([file_name, str(stamp), date])

    file_name = '.'.join([file_name, suffix])
    return file_name


rule_dt = re.compile(r"(.+?)__(?P<dtime>.+?)__(?P<date>.+?)")


def get_dtime_from_name(file_name):
    return float(rule_dt.search(file_name).group('dtime'))


# folder
def make_folder(*path_ls):
    """接收并尝试建立folder，返回成功建立的path"""

    success_path = []
    for path in path_ls:
        if not os.path.isdir(path):  # 不存在则建立
            os.makedirs(path)
            success_path.append(path)
    return success_path


def remove_all(*path):
    """folder_path,...,file_name"""

    path_com = os.path.join(*path)
    if os.path.isfile(path_com):  # 移除文件
        try:
            os.remove(path_com)
            # print("文件%s已移除" % path_com)
            return True
        except Exception as e:
            print("文件删除失败！")
            print(Exception, ":", e)
            return False
    elif os.path.isdir(path_com):  # 移除文件夹
        try:
            os.removedirs(path_com)
            # print("文件夹%s已移除" % path_com)
            return True
        except Exception as e:
            print("文件夹删除失败！")
            print(Exception, ":", e)
            return False


class Folder_Manager:

    def __init__(self, dir_=None):
        self.dir_ls = dir_ if dir_ else []  # 用于记录已经存在的目录

    def touch(self, dir_):
        if dir_ in self.dir_ls:
            return True
        elif not os.path.isdir(dir_):
            os.mkdir(dir_)
            self.dir_ls.append(dir_)


# path
def convert_path_to_standard_form(path):
    """把任意路径path转换成当前系统的格式"""

    seps = r'\/'
    sep_other = seps.replace(os.sep, '')
    path = path.replace(sep_other, os.sep)
    while os.sep * 2 in path:
        path.replace(os.sep * 2, os.sep)
    return path


def get_relative_path(base_path, long_path):
    """
    获取相对路径
    relative_path 为 a/b/c 形式
    """

    if base_path in long_path:
        relative_path = long_path.replace(base_path, '')
        relative_path = relative_path[1:] if relative_path[0] == os.sep else relative_path
        return relative_path
    else:
        return long_path


# 获取path目录中，带指定后缀和flag的文件的路径
def search_file(folder, suffix_ls=None, flag_ls=None, case_sensitive=False):
    """
    return all file_path_dict with specific suffix in folder (Hierarchical)
    :param folder: 待搜索的目录，要求是绝对路径，而且是为 a/b/c 形式
    :param suffix_ls: 后缀列表
    :param flag_ls: 文件名中的flag
    :param case_sensitive: 区分大小写（默认不区分）
    suffix_ls 和 flag_ls 不指定时表示不开启筛选
    :return: 各级path及其下面符合条件的文件名 [{"folder": folder, "filename_ls": file_ls}, ……]
    """

    dir_ls = os.listdir(folder)  # 获取path目录下的文件和文件夹
    file_ls = []
    dict_ = []
    for dir_ in dir_ls:
        pathTmp = os.path.join(folder, dir_)
        if os.path.isdir(pathTmp):  # 如是目录,则递归查找
            dict_ += search_file(pathTmp, suffix_ls, flag_ls)
        else:  # 不是目录,则比较后缀名
            file_ls.append(dir_)  # 先加进来，后面再剔除

            if not case_sensitive:
                dir_ = dir_.lower()
            name, suffix = os.path.splitext(dir_)
            if suffix_ls and suffix not in suffix_ls:  # suffix 筛选
                file_ls.pop(-1)
            elif flag_ls:  # flag 筛选
                bingo = False
                for flag in flag_ls:
                    if flag in name:
                        bingo = True
                if not bingo:
                    file_ls.pop(-1)
    return [{"folder": folder, "filename_ls": file_ls}] + dict_


def search_file_flat(folder, suffix_ls=None, flag_ls=None, case_sensitive=False):
    """
    return all file_path_dict with specific suffix in folder (Regardless of the hierarchy)
    输入参数介绍请参见 search_file() 方法
    """

    file_path_ls = []
    folder_filename_dict_ls = search_file(folder, suffix_ls, flag_ls, case_sensitive)
    for folder_filename_dict in folder_filename_dict_ls:
        _folder_ = folder_filename_dict.get("folder")
        for _filename_ in folder_filename_dict.get("filename_ls"):
            file_path = os.path.join(_folder_, _filename_)
            file_path_ls.append(file_path)
    return file_path_ls


# 修改文件名后缀
def change_suffix(aim_suffix, *path):
    """
    Change filename suffix
    """

    path_old = os.path.join(*path)
    # 安全锁
    if not os.path.isfile(path_old):
        return False

    _, file_name = os.path.split(path_old)
    # 换名
    name, suffix = os.path.splitext(file_name)
    new_name = name + aim_suffix
    path_new = os.path.join(path, new_name)
    if os.path.isfile(path_new):  # 目标文件已存在
        os.remove(path_old)
    else:
        os.rename(path_old, path_new)
    return path_new


# read and write
# markdown
def read_markdown(*path):
    """folder_path,...,file_name"""

    try:
        path_com = os.path.join(*path)
        if os.path.isfile(path_com):
            with open(path_com, 'r', encoding='utf-8') as file:
                content = file.read()
            print(path_com, 'read.')
            return content
        else:
            print("File name error！")
            return None
    except Exception as e:
        print("failed to read")
        print(Exception, ":", e)
        return None


def write_markdown(content, *path):
    """content,folder_path,file_name"""

    if content:
        try:
            path_com = os.path.join(*path)
            with open(path_com, 'w', encoding='utf-8') as fff:
                fff.write(content)
            print(path_com, 'wrote.')
            return path_com
        except Exception as e:
            print("failed to write")
            print(Exception, ":", e)
            return None
    else:
        return None


if __name__ == '__main__':
    print(search_file_flat(r"C:\Git\My_git_blog\my_blog\source", [".md"]))
