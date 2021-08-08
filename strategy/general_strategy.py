# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 7:44
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : general_strategy.py
# @Software: PyCharm
# @Description: general strategy
from strategy.base_strategy import base_strategy


class general_strategy(base_strategy):

    def best_h_index_arg(self):
        self.debug_print()
        best_delta_h = 0
        best_index = -1
        best_args = []

        for hand_card_index, hand_card in enumerate(self.my_hand_cards):
            delta_h = 0
            args = []

            if hand_card.current_cost > self.my_last_mana:
                self.debug_print(f"跳过第[{hand_card_index}]张卡牌({hand_card.name})")
                continue

            detail_card = hand_card.detail_card
            if detail_card is None:
                if hand_card.cardtype == self.CARD_MINION and not hand_card.battlecry:
                    delta_h, *args = self.MinionNoPoint.best_h_and_arg(self, hand_card_index)
                    self.debug_print(f"(默认行为) card[{hand_card_index}]({hand_card.name}) "
                                f"delta_h: {delta_h}, *args: {[]}")
                else:
                    self.debug_print(f"卡牌[{hand_card_index}]({hand_card.name})无法评判")
            else:
                delta_h, *args = detail_card.best_h_and_arg(self, hand_card_index)
                self.debug_print(f"(手写行为) card[{hand_card_index}]({hand_card.name}) "
                            f"delta_h: {delta_h}, *args: {args}")

            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = hand_card_index
                best_args = args

        self.debug_print(f"决策结果: best_delta_h:{best_delta_h}, "
                    f"best_index:{best_index}, best_args:{best_args}")
        self.debug_print()
        return best_delta_h, best_index, best_args

