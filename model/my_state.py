# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 7:31
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : my_state.py
# @Software: PyCharm
# @Description: my game state info

class my_state:
    def __init__(self):
        self.my_total_mana = 0
        self.my_used_mana = 0
        self.my_temp_mana = 0
        self.my_hand_cards = []
        self.my_minions = []
        self.my_graveyard = []

    @property
    def my_last_mana(self):
        return self.my_total_mana - self.my_used_mana + self.my_temp_mana

    @property
    def my_hand_card_num(self):
        return len(self.my_hand_cards)

    @property
    def my_minion_num(self):
        return len(self.my_minions)
