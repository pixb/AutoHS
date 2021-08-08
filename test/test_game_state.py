# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 6:32
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : test_game_state.py
# @Software: PyCharm
# @Description: game state test case

from unittest import TestCase
from model.game_state import *
from model.log_op import log_iter_func

game_state = GameState()
log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)

def update_game_state():
    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        sys_print("未找到Power.log，请启动炉石并开始对战")
        return False

    for log_line_container in log_container.message_list:
        ok = update_state(game_state, log_line_container)
        # if not ok:
        #     return False

    if DEBUG_FILE_WRITE:
        with open("../log/game_state_snapshot.txt", "w", encoding="utf8") as f:
            f.write(str(game_state))

    # 注意如果Power.log没有更新, 这个函数依然会返回. 应该考虑到game_state只是被初始化
    # 过而没有进一步更新的可能
    if game_state.game_entity_id == 0:
        return False
    print("game_state.my_entity:{}".format(game_state.my_entity))
    return True


class Test(TestCase):
    def test_update_game_state(self):
        ok = update_game_state()
        print("update_game_state()={}".format(ok))
        return True
