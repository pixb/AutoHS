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
        self.oppo_hero = None
        self.oppo_weapon = None
        self.oppo_hero_power = None

    @property
    def oppo_minion_num(self):
        return len(self.oppo_minions)

    # 用卡费体系算启发值
    @property
    def oppo_heuristic_value(self):
        total_h_val = self.oppo_hero.heuristic_val
        if self.oppo_weapon:
            total_h_val += self.oppo_weapon.heuristic_val
        for minion in self.oppo_minions:
            total_h_val += minion.heuristic_val
        return total_h_val
