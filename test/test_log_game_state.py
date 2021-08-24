# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 6:32
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : test_game_state.py
# @Software: PyCharm
# @Description: game state test case

from unittest import TestCase

from hslog import LogParser
from hslog.export import EntityTreeExporter

from model.game_state import *
from model.log_op import log_iter_func
from model.t_game_state import t_game_state

game_state = None


def update_log_game_state():
    global game_state
    game_state = t_game_state()
    return game_state.init()


class Test(TestCase):
    def test_log_state(self):
        global game_state
        ok = update_log_game_state()
        if not ok:
            print("init error....")
            return
        print("~~~update_game_state()={}".format(ok))
        print("~~~update_game_state() turns={}".format(game_state.game_num_turns_in_play))
        print("~~~~update_game_state() , hand card count:{}\n".format(game_state.my_state.my_hand_card_num))
        return True
