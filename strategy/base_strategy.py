# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 7:22
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : base_strategy.py
# @Software: PyCharm
# @Description: 策略接口
import abc

import random

from card.basic_card import MinionNoPoint
from strategy.strategy_entity import *
from view import click


class base_strategy(metaclass=abc.ABCMeta):
    def __init__(self, game_state=None, a_game_state=None):
        self.debug_print_out_state(game_state)

    def debug_print_battlefield(self, game_state):
        if not DEBUG_PRINT:
            return

        debug_print("对手英雄:")
        debug_print("    " + str(game_state.oppo_state.oppo_hero))
        debug_print(f"技能:")
        debug_print("    " + game_state.oppo_state.oppo_hero_power.name)
        if game_state.oppo_state.oppo_weapon:
            debug_print("头上有把武器:")
            debug_print("    " + str(game_state.oppo_state.oppo_weapon))
        if game_state.oppo_state.oppo_minion_num > 0:
            debug_print(f"对手有{game_state.oppo_state.oppo_minion_num}个随从:")
            for minion in game_state.oppo_state.oppo_minions:
                debug_print("    " + str(minion))
        else:
            debug_print(f"对手没有随从")
        debug_print(f"总卡费启发值: {game_state.oppo_state.oppo_heuristic_value}")

        debug_print()

        debug_print("我的英雄:")
        debug_print("    " + str(game_state.my_state.my_hero))
        debug_print(f"技能:")
        debug_print("    " + game_state.my_state.my_hero_power.name)
        if game_state.my_state.my_weapon:
            debug_print("头上有把武器:")
            debug_print("    " + str(game_state.my_state.my_weapon))
        if game_state.my_state.my_minion_num > 0:
            debug_print(f"我有{game_state.my_state.my_minion_num}个随从:")
            for minion in game_state.my_state.my_minions:
                debug_print("    " + str(minion))
        else:
            debug_print("我没有随从")
        debug_print(f"总卡费启发值: {game_state.my_state.my_heuristic_value}")

    def debug_print_out_state(self, game_state):
        if not DEBUG_PRINT:
            return

        debug_print(f"game_state 对手墓地:")
        debug_print("    " + ", ".join([entity.name for entity in game_state.oppo_state.oppo_graveyard]))
        debug_print(f"game_state 对手有{game_state.oppo_state.oppo_hand_card_num}张手牌")

        self.debug_print_battlefield(game_state)
        debug_print()

        debug_print(f"game_state 水晶: {game_state.my_state.my_last_mana}/{game_state.my_state.my_total_mana}")
        debug_print(f"game_state 我有{game_state.my_state.my_hand_card_num}张手牌:")
        for hand_card in game_state.my_state.my_hand_cards:
            debug_print(f"    [{hand_card.zone_pos}] {hand_card.name} "
                        f"cost:{hand_card.current_cost}")
        debug_print(f"我的墓地:")
        debug_print("    " + ", ".join([entity.name for entity in game_state.my_state.my_graveyard]))



    @property
    def heuristic_value(self):
        return round(self.my_heuristic_value - self.oppo_heuristic_value, 3)

    @property
    def min_cost(self, game_state):
        minium = 100
        for hand_card in game_state.my_state.my_hand_cards:
            minium = min(minium, hand_card.current_cost)
        return minium



    def fight_between(self, oppo_index, my_index, game_state):
        oppo_minion = game_state.oppo_state.oppo_minions[oppo_index]
        my_minion = game_state.my_state.my_minions[my_index]

        if oppo_minion.get_damaged(my_minion.attack):
            game_state.oppo_state.oppo_minions.pop(oppo_index)

        if my_minion.get_damaged(oppo_minion.attack):
            game_state.my_state.my_minions.pop(my_index)

    def random_distribute_damage(self, damage, oppo_index_list, my_index_list):
        if len(oppo_index_list) == len(my_index_list) == 0:
            return

        random_x = random.randint(0, len(oppo_index_list) + len(my_index_list) - 1)

        if random_x < len(oppo_index_list):
            oppo_index = oppo_index_list[random_x]
            minion = self.oppo_minions[oppo_index]
            if minion.get_damaged(damage):
                self.oppo_minions.pop(oppo_index)
        else:
            my_index = my_index_list[random_x - len(oppo_index_list)]
            minion = self.my_minions[my_index]
            if minion.get_damaged(damage):
                self.my_minions.pop(my_index)

    def get_best_attack_target(self, game_state):
        touchable_oppo_minions = game_state.oppo_state.touchable_oppo_minions
        has_taunt = game_state.oppo_state.oppo_has_taunt
        beat_face_win = game_state.my_state.my_total_attack >= game_state.oppo_state.oppo_hero.health

        max_delta_h_val = 0
        max_my_index = -2
        max_oppo_index = -2
        min_attack = 0

        # 枚举每一个己方随从
        for my_index, my_minion in enumerate(game_state.my_state.my_minions):
            if not my_minion.can_attack_minion:
                continue

            # 如果没有墙,自己又能打脸,应该试一试
            if not has_taunt and my_minion.can_beat_face:
                if beat_face_win:
                    debug_print(f"攻击决策: [{my_index}]({my_minion.name})->"
                                f"[-1]({game_state.oppo_state.oppo_hero.name}) "
                                f"斩杀了")
                    return my_index, -1

                tmp_delta_h = game_state.oppo_state.oppo_hero.delta_h_after_damage(my_minion.attack)

                debug_print(f"攻击决策: [{my_index}]({my_minion.name})->"
                            f"[-1]({game_state.oppo_state.oppo_hero.name}) "
                            f"delta_h_val:{tmp_delta_h}")

                if tmp_delta_h > max_delta_h_val:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = my_index
                    max_oppo_index = -1
                    min_attack = 999

            for oppo_minion in touchable_oppo_minions:
                oppo_index = oppo_minion.zone_pos - 1

                tmp_delta_h = 0
                tmp_delta_h -= MY_DELTA_H_FACTOR * \
                               my_minion.delta_h_after_damage(oppo_minion.attack)
                tmp_delta_h += OPPO_DELTA_H_FACTOR * \
                               oppo_minion.delta_h_after_damage(my_minion.attack)

                debug_print(f"攻击决策：[{my_index}]({my_minion.name})->"
                            f"[{oppo_index}]({oppo_minion.name}) "
                            f"delta_h_val: {tmp_delta_h}")

                if tmp_delta_h > max_delta_h_val or \
                        tmp_delta_h == max_delta_h_val and my_minion.attack < min_attack:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = my_index
                    max_oppo_index = oppo_index
                    min_attack = my_minion.attack

        # 试一试英雄攻击
        if game_state.my_state.my_hero.can_attack:
            if not has_taunt:
                if beat_face_win:
                    debug_print(f"攻击决策: [-1]({game_state.my_state.my_hero.name})->"
                                f"[-1]({game_state.oppo_state.oppo_hero.name}) "
                                f"斩杀了")
                    return -1, -1

            for oppo_minion in touchable_oppo_minions:
                oppo_index = oppo_minion.zone_pos - 1

                tmp_delta_h = 0
                tmp_delta_h += OPPO_DELTA_H_FACTOR * \
                               oppo_minion.delta_h_after_damage(game_state.my_state.my_hero.attack)
                tmp_delta_h -= game_state.my_state.my_hero.delta_h_after_damage(oppo_minion.attack)
                if game_state.my_state.my_weapon is not None:
                    tmp_delta_h -= game_state.my_state.my_weapon.attack

                debug_print(f"攻击决策: [-1]({game_state.my_state.my_hero.name})->"
                            f"[{oppo_index}]({oppo_minion.name}) "
                            f"delta_h_val: {tmp_delta_h}")

                if tmp_delta_h >= max_delta_h_val:
                    max_my_index = -1
                    max_oppo_index = oppo_index

        debug_print(f"最终决策: max_my_index: {max_my_index}, "
                    f"max_oppo_index: {max_oppo_index}")

        return max_my_index, max_oppo_index

    def my_entity_attack_oppo(self, game_state, my_index, oppo_index):
        if my_index == -1:
            if oppo_index == -1:
                click.hero_beat_hero()
            else:
                click.hero_beat_minion(oppo_index, game_state.oppo_state.oppo_minion_num)
        else:
            if oppo_index == -1:
                click.minion_beat_hero(my_index, game_state.my_state.my_minion_num)
            else:
                click.minion_beat_minion(my_index, game_state.my_state.my_minion_num,
                                         oppo_index, game_state.oppo_state.oppo_minion_num)


    def copy_new_one(self, game_state):
        # TODO: 有必要deepcopy吗
        tmp = copy.deepcopy(self)
        for i in range(game_state.oppo_state.oppo_minion_num):
            tmp.oppo_minions[i] = copy.deepcopy(game_state.oppo_state.oppo_minions[i])
        for i in range(game_state.my_state.my_minion_num):
            tmp.my_minions[i] = copy.deepcopy(game_state.my_state.my_minions[i])
        for i in range(game_state.my_state.my_hand_card_num):
            tmp.my_hand_cards[i] = copy.deepcopy(game_state.my_state.my_hand_cards[i])
        return tmp

    @abc.abstractmethod
    def best_h_index_arg(self):
        pass

    def use_best_entity(self, game_state, index, args):
        if index == -1:
            debug_print("将使用技能")
            hero_power = game_state.my_state.my_detail_hero_power
            hero_power.use_with_arg(self, game_state, -1, *args)
        else:
            self.use_card(game_state, index, *args)

    # 会返回这张卡的cost
    def use_card(self, game_state, index, *args):
        hand_card = game_state.my_state.my_hand_cards[index]
        detail_card = hand_card.detail_card
        debug_print(f"将使用卡牌[{index}] {hand_card.name}")
        debug_print()

        if detail_card is None:
            MinionNoPoint.use_with_arg(self, game_state, index, *args)
        else:
            detail_card.use_with_arg(self, game_state, index, *args)

        game_state.my_state.my_hand_cards.pop(index)
        return hand_card.current_cost



# if __name__ == "__main__":
#     keyboard.add_hotkey("ctrl+q", sys.exit)
#
#     log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
#     state = GameState()
#
#     while True:
#         log_container = next(log_iter)
#         if log_container.length > 0:
#             for x in log_container.message_list:
#                 update_state(state, x)
#             strategy_state = base_strategy(state)
#
#             with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
#                 f.write(str(state))
#
#             mine_index, oppo_index = strategy_state.get_best_attack_target()
#             debug_print(f"我的决策是: mine_index: {mine_index}, oppo_index: {oppo_index}")
#
#             if mine_index != -1:
#                 if oppo_index == -1:
#                     click.minion_beat_hero(mine_index, strategy_state.my_minion_num)
#                 else:
#                     click.minion_beat_minion(mine_index, strategy_state.my_minion_num,
#                                              oppo_index, strategy_state.oppo_minion_num)
