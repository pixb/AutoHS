# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 7:31
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : my_state.py
# @Software: PyCharm
# @Description: my game state info

class oppo_state:
    def __init__(self):
        self.oppo_graveyard = []
        self.oppo_minions = []
        self.oppo_hand_card_num = 0

    @property
    def oppo_minion_num(self):
        return len(self.oppo_minions)
