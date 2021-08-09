# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 7:31
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : my_state.py
# @Software: PyCharm
# @Description: my game state info

class my_state:
    def __init__(self):
        self.my_hero = None
        self.my_hero_power = None
        self.my_weapon = None
        self.my_total_mana = 0
        self.my_used_mana = 0
        self.my_temp_mana = 0
        self.my_hand_cards = []
        self.my_minions = []
        self.my_graveyard = []
        self.can_use_power = False

    @property
    def my_last_mana(self):
        return self.my_total_mana - self.my_used_mana + self.my_temp_mana

    @property
    def my_hand_card_num(self):
        return len(self.my_hand_cards)

    @property
    def my_minion_num(self):
        return len(self.my_minions)

    @property
    def my_heuristic_value(self):
        total_h_val = self.my_hero.heuristic_val
        if self.my_weapon:
            total_h_val += self.my_weapon.heuristic_val
        for minion in self.my_minions:
            total_h_val += minion.heuristic_val
        return total_h_val

    @property
    def my_detail_hero_power(self):
        return self.my_hero_power.detail_hero_power

    def my_total_spell_power(self):
        return sum([minion.spell_power for minion in my_state.my_minions])
