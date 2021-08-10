# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 7:44
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : never_power_strategy.py
# @Software: PyCharm
# @Description: general strategy
from strategy.base_strategy import base_strategy
from utils.print_info import debug_print


class never_power_strategy(base_strategy):

    def best_h_index_arg(self, game_state):
        debug_print()
        best_delta_h = 0
        best_index = -1
        best_args = []
        return best_delta_h, best_index, best_args


