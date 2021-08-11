# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 7:31
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : t_my_state.py
# @Software: PyCharm
# @Description: my game state info

class t_oppo_state:
    def __init__(self):
        self.oppo_graveyard = []
        self.oppo_minions = []
        self.oppo_hand_card_num = 0
        self.oppo_hero = None
        self.oppo_weapon = None
        self.oppo_hero_power = None

    def update(self, game_state):
        self.oppo_hand_card_num = 0
        self.oppo_minions.clear()
        self.oppo_graveyard.clear()

        for entity in game_state.entity_dict.values():
            if entity.query_tag("ZONE") == "HAND":
                if not game_state.is_my_entity(entity):
                    self.oppo_hand_card_num += 1

            elif entity.zone == "PLAY":
                if entity.cardtype == "MINION":
                    minion = entity.corresponding_entity
                    if not game_state.is_my_entity(entity):
                        self.oppo_minions.append(minion)

                elif entity.cardtype == "HERO":
                    hero = entity.corresponding_entity
                    if not game_state.is_my_entity(entity):
                        self.oppo_hero = hero

                elif entity.cardtype == "HERO_POWER":
                    hero_power = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.oppo_hero_power = hero_power

                elif entity.cardtype == "WEAPON":
                    weapon = entity.corresponding_entity
                    if not game_state.is_my_entity(entity):
                        self.oppo_weapon = weapon

            elif entity.zone == "GRAVEYARD":
                if not game_state.is_my_entity(entity):
                    self.oppo_graveyard.append(entity)

        # 从这里取用户的一些信息
        self.oppo_minions.sort(key=lambda temp: temp.zone_pos)

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

    @property
    def touchable_oppo_minions(self):
        ret = []

        for oppo_minion in self.oppo_minions:
            if oppo_minion.taunt and not oppo_minion.stealth:
                ret.append(oppo_minion)

        if len(ret) == 0:
            for oppo_minion in self.oppo_minions:
                if not oppo_minion.stealth:
                    ret.append(oppo_minion)

        return ret

    @property
    def oppo_has_taunt(self):
        for oppo_minion in self.oppo_minions:
            if oppo_minion.taunt and not oppo_minion.stealth:
                return True

        return False
