# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 6:32
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : test_battling.py
# @Software: PyCharm
# @Description: game battling test case

from strategy.base_strategy import *
from strategy.general_strategy import general_strategy
from test_game_state import *
from view import click


def update_strategy_state():
    print("Battling start...")
    ok = update_game_state()
    print("update_game_state()={}".format(ok))
    print("state:\n"
          "\t game_state.is_end:{}\n"
          "\t PLAYSTATE:{}\n"
          "\t game_state.is_my_turn:{}\n"
          "\t game_state.game_num_turns_in_play:{}\n"
          .format(game_state.is_end,
                  game_state.my_entity.query_tag("PLAYSTATE"),
                  game_state.is_my_turn,
                  game_state.game_num_turns_in_play))
    return general_strategy(game_state)


def use_card():
    # 考虑要不要出牌
    strategy_state = update_strategy_state()
    delta_h, index, args = strategy_state.best_h_index_arg()
    print("put card:\n"
          "\t delta_h:{}\n"
          "\t index:{}\n"
          "\t args:{}\n"
          .format(delta_h, index, args))
    if delta_h > 0:
        strategy_state.use_card(index, *args)


def use_power():
    strategy_state = update_strategy_state()
    # 考虑要不要用技能
    hero_power = strategy_state.my_detail_hero_power
    if hero_power and strategy_state.my_last_mana >= 2:
        delta_h, *args = hero_power.best_h_and_arg(strategy_state, -1)
        debug_print(str(delta_h) + str(args))
        if delta_h > 0:
            hero_power.use_with_arg(strategy_state, -1, *args)

    print("power:\n"
          "\t hero_power:{}\n"
          "\t strategy_state.my_last_mana:{}\n"
          .format(hero_power, strategy_state.my_last_mana))


def minion_beat():
    strategy_state = update_strategy_state()
    mine_index, oppo_index = strategy_state.get_best_attack_target()
    if mine_index != -1:
        if oppo_index == -1:
            click.minion_beat_hero(mine_index, strategy_state.my_minion_num)
        else:
            click.minion_beat_minion(mine_index, strategy_state.my_minion_num,
                                     oppo_index, strategy_state.oppo_minion_num)


class Test(TestCase):
    def test_update_strategy_state(self):
        update_strategy_state()

    def test_use_card(self):
        use_card()
        return True

    def test_use_power(self):
        use_power()
        return True

    def test_minion_beat(self):
        minion_beat()
        return True

    def test_end_turn(self):
        click.end_turn()
        return True
