# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 7:44
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : general_strategy.py
# @Software: PyCharm
# @Description: general strategy
from card.basic_card import MinionNoPoint
from constants.constants import *
from strategy.base_strategy import base_strategy
from utils.print_info import debug_print


class general_strategy(base_strategy):

    def best_h_index_arg(self, game_state):
        debug_print()
        best_delta_h = 0
        best_index = -2
        best_args = []

        # 考虑使用手牌
        for hand_card_index, hand_card in enumerate(game_state.my_state.my_hand_cards):
            delta_h = 0
            args = []

            if hand_card.current_cost > game_state.my_state.my_last_mana:
                debug_print(f"卡牌-[{hand_card_index}]({hand_card.name}) 跳过")
                continue

            detail_card = hand_card.detail_card
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    delta_h, *args = MinionNoPoint.best_h_and_arg(self, game_state, hand_card_index)
                    debug_print(f"卡牌-[{hand_card_index}]({hand_card.name}) "
                                f"delta_h: {delta_h}, *args: {[]} (默认行为) ")
                else:
                    debug_print(f"卡牌[{hand_card_index}]({hand_card.name})无法评判")
            else:
                delta_h, *args = detail_card.best_h_and_arg(self, game_state, hand_card_index)
                debug_print(f"卡牌-[{hand_card_index}]({hand_card.name}) "
                            f"delta_h: {delta_h}, *args: {args} (手写行为)")

            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = hand_card_index
                best_args = args

        # 考虑使用英雄技能
        if game_state.my_state.my_last_mana >= 2 and \
                game_state.my_state.my_detail_hero_power and \
                not game_state.my_state.my_hero_power.exhausted:
            hero_power = game_state.my_state.my_detail_hero_power

            delta_h, *args = hero_power.best_h_and_arg(self, game_state, -1)

            debug_print(f"技能-[-1]({game_state.my_state.my_hero_power.name}) "
                        f"delta_h: {delta_h} "
                        f"*args: {args}")

            if delta_h > best_delta_h:
                best_index = -1
                best_args = args
        else:
            debug_print(f"技能-[-1]({game_state.my_state.my_hero_power.name}) 跳过")

        debug_print(f"决策结果: best_delta_h:{best_delta_h}, "
                    f"best_index:{best_index}, best_args:{best_args}")
        debug_print()
        return best_index, best_args
