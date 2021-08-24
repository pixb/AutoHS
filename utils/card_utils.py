# -*- coding: utf-8 -*-
# @Time    : 2021/8/15 2:10
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : card_utils.py
# @Software: PyCharm
# @Description:
from hearthstone.enums import GameTag


def get_card_cost(card):
    if card is None:
        return -1
    return card.tags.get(GameTag.TAG_LAST_KNOWN_COST_IN_HAND, -1)
