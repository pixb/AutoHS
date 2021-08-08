# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 18:09
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : main_view.py
# @Software: PyCharm
# @Description: 只写和View相关的代码，例如输出提示信息，点击等操作都要定义到这里
import time

from print_info import info_print


class main_view(object):

    def show_time(slef):
        info_print("Now the time is " +
                   time.strftime("%m-%d %H:%M:%S", time.localtime()))
        return time.time()
