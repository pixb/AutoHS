# -*- coding: utf-8 -*-
# @Time    : 2021/8/8 18:07
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : main_controller.py
# @Software: PyCharm
# @Description: main controller 控制曾代码可以乱一点，主要为了分离数据和View，留下来的作为控制逻辑代码
import random
import sys
import time

import keyboard
from hearthstone.enums import GameTag

from card.id2card import ID2CARD_DICT
from model.log_op import log_iter_func
from model.game_state import check_name, GameState, update_state
from model.main_model import main_model
from model.t_game_state import t_game_state
from strategy.never_power_strategy import never_power_strategy
from utils.card_utils import get_card_cost
from utils.print_info import *
from strategy.general_strategy import general_strategy
from view import click, get_screen
from view.main_view import main_view

time_begin = 0.0
game_count = 0
win_count = 0
quitting_flag = False
game_state = GameState()
a_game_state = t_game_state()
log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
strategy = None
choose_hero_count = 0


def get_strategy_mode():
    strategies = {
        0: never_power_strategy(game_state, a_game_state),
        1: general_strategy(game_state, a_game_state)
    }
    return strategies.get(GAME_STRATEGY)
    # return strategy


def system_exit():
    global quitting_flag
    sys_print(f"一共完成了{game_count}场对战, 赢了{win_count}场")
    print_info_close()
    quitting_flag = True
    sys.exit(0)


def update_game_state():
    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        return False

    for log_line_container in log_container.message_list:
        ok = update_state(game_state, log_line_container)
        # if not ok:
        #     return False
    if DEBUG_FILE_WRITE:
        with open("./log/game_state_snapshot.txt", "w", encoding="utf8") as f:
            f.write(str(game_state))

    # 注意如果Power.log没有更新, 这个函数依然会返回. 应该考虑到game_state只是被初始化
    # 过而没有进一步更新的可能
    if game_state.game_entity_id == 0:
        return False

    if a_game_state.game_entity_id == 0:
        return False

    return True


class main_controller(object):

    def __init__(self):
        self._view = main_view()
        self._model = main_model()
        self._fsm_state = ""

    def AutoHS_automata(self):

        while 1:
            if quitting_flag:
                sys.exit(0)
            if self._fsm_state == "":
                self._fsm_state = get_screen.get_state()
            self._fsm_state = self.FSM_dispatch(self._fsm_state)

    def MainMenuAction(self):

        self.print_out()
        time.sleep(30)
        while True:
            if quitting_flag:
                sys.exit(0)

            click.enter_battle_mode()
            time.sleep(5)

            state = get_screen.get_state()

            # 重新连接对战之类的
            if state == FSM_BATTLING:
                ok = update_game_state()
                if ok and game_state.available:
                    return FSM_BATTLING

            if state == FSM_BATTLING:
                ok = a_game_state.init()
                if ok and a_game_state.available:
                    return FSM_BATTLING

            if state == FSM_CHOOSING_HERO:
                return FSM_CHOOSING_HERO

    def ChoosingHeroAction(self):
        self.print_out()
        time.sleep(2)
        click.match_opponent()
        time.sleep(1)
        return FSM_MATCHING

    def MatchingAction(self):
        self.print_out()
        loop_count = 0

        while True:
            time.sleep(STATE_CHECK_INTERVAL)

            click.commit_error_report()

            if GAME_STRATEGY == 0:
                return FSM_CHOOSING_CARD

            ok = update_game_state()
            if ok:
                if not game_state.is_end:
                    return FSM_CHOOSING_CARD

            aok = a_game_state.init()
            if aok and a_game_state.is_end:
                return FSM_CHOOSING_CARD

            curr_state = get_screen.get_state()
            if curr_state == FSM_CHOOSING_HERO:
                return FSM_CHOOSING_HERO

            loop_count += 1
            if loop_count >= 60:
                warn_print("Time out in Matching Opponent")
                return FSM_ERROR

    def ChoosingCardAction(self):
        global choose_hero_count
        choose_hero_count = 0
        global strategy

        self.print_out()
        time.sleep(21)
        loop_count = 0
        has_print = 0

        if GAME_STRATEGY == 0:
            time.sleep(20)
            click.commit_choose_card()
            return FSM_BATTLING

        while True:
            ok = update_game_state()
            aok = a_game_state.init()

            print("&&&&&&&&&&&&&&&&&&&&&& Choosing Card Start &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("game state, turns:{}\n".format(game_state.game_num_turns_in_play))
            print("a game state, turns:{}\n".format(a_game_state.game_num_turns_in_play))

            print("&&&&&&&&&&&&&&&&&&&&&&&&  Choosing Card End  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

            # if not ok:
            #     warn_print("update_game_state() ERROR")
            #     return FSM_ERROR
            # if game_state.game_num_turns_in_play > 0:
            #     return FSM_BATTLING
            # if game_state.is_end:
            #     return FSM_QUITTING_BATTLE
            game_state.update_user_state()

            if not aok:
                warn_print("update_a_game_state() ERROR")
                return FSM_ERROR
            if a_game_state.game_num_turns_in_play > 0:
                print("Battling turns:{}".format(a_game_state.game_num_turns_in_play))
                return FSM_BATTLING
            if a_game_state.is_end:
                return FSM_QUITTING_BATTLE

            strategy = get_strategy_mode()
            # hand_card_num = game_state.my_state.my_hand_card_num
            hand_card_num = a_game_state.my_state.my_hand_card_num
            print("game_state，hand card count:{}\n".format(game_state.my_state.my_hand_card_num))
            print("a_game_state, hand card count:{}\n".format(a_game_state.my_state.my_hand_card_num))

            # 等待被替换的卡牌 ZONE=HAND
            # 注意后手时幸运币会作为第五张卡牌算在手牌里, 故只取前四张手牌
            # 但是后手时 hand_card_num 仍然是 5
            for my_hand_index, my_hand_card in \
                    enumerate(a_game_state.my_state.my_hand_cards[:4]):
                # detail_card = my_hand_card.detail_card
                detail_card = ID2CARD_DICT.get(my_hand_card.card_id, None)

                if detail_card is None:
                    cost = get_card_cost(my_hand_card)
                    print("&&&&&&&&&&&&&&&&&&  detail_card:{}, cost:{}".format(detail_card, cost))
                    if cost == -1:
                        should_keep_in_hand = True
                    else:
                        should_keep_in_hand = \
                            cost <= REPLACE_COST_BAR
                else:
                    should_keep_in_hand = \
                        detail_card.keep_in_hand()

                if not should_keep_in_hand:
                    click.replace_starting_card(my_hand_index, hand_card_num)

            click.commit_choose_card()

            loop_count += 1
            if loop_count >= 60:
                warn_print("Time out in Choosing Opponent")
                return FSM_ERROR
            time.sleep(STATE_CHECK_INTERVAL)

    def Battling(self):
        global win_count
        global game_state
        global a_game_state
        global strategy

        self.print_out()

        not_mine_count = 0
        mine_count = 0
        last_controller_is_me = False

        while True:
            if quitting_flag:
                sys.exit(0)

            if GAME_STRATEGY == 0:
                self._view.use_power_no_point()
                click.end_turn()
                time.sleep(3)
                if get_screen.get_state() == FSM_CHOOSING_HERO:
                    return FSM_CHOOSING_HERO
                continue

            ok = update_game_state()
            if not ok:
                warn_print("update_game_state() ERROR")
                return FSM_ERROR

            if game_state.is_end:
                if game_state.my_entity.query_tag("PLAYSTATE") == "WON":
                    win_count += 1
                    info_print("你赢得了这场对战")
                else:
                    info_print("你输了")
                return FSM_QUITTING_BATTLE

            # aok = a_game_state.init()
            # if not aok:
            #     warn_print("update_t_game_state() ERROR")
            #     return FSM_ERROR
            # if a_game_state.is_end:
            #     if a_game_state.my_state.is_end_win():
            #         win_count += 1
            #         info_print("你赢得了这场对战")
            #     else:
            #         info_print("你输了")
            #     return FSM_QUITTING_BATTLE

            # 在对方回合等就行了
            if not game_state.is_my_turn:
                last_controller_is_me = False
                mine_count = 0

                not_mine_count += 1
                if not_mine_count >= 400:
                    warn_print("Time out in Opponent's turn")
                    return FSM_ERROR

                continue

            # 接下来考虑在我的回合的出牌逻辑

            # 如果是这个我的回合的第一次操作
            if not last_controller_is_me:
                time.sleep(5.5)
                # 在游戏的第一个我的回合, 发一个你好
                # game_num_turns_in_play在每一个回合开始时都会加一, 即
                # 后手放第一个回合这个数是2
                if a_game_state.game_num_turns_in_play <= 2:
                    click.emoj(0)
                else:
                    # 在之后每个回合开始时有概率发表情
                    if random.random() < EMOJ_RATIO:
                        click.emoj()

            last_controller_is_me = True
            not_mine_count = 0
            mine_count += 1

            if mine_count >= 20:
                if mine_count >= 40:
                    warn_print("Battling mine_count >= 40")
                    return FSM_ERROR
                click.end_turn()
                click.commit_error_report()
                click.cancel_click()
                time.sleep(STATE_CHECK_INTERVAL)

            debug_print("-" * 80)
            game_state.update_user_state()
            a_game_state.init()
            strategy = get_strategy_mode()

            # 考虑要不要出牌
            index, args = strategy.best_h_index_arg(game_state)

            # index == -1 代表使用技能, -2 代表不出牌
            if index != -2:
                strategy.use_best_entity(game_state, index, args)
                continue

            # 如果不出牌, 考虑随从怎么打架
            my_index, oppo_index = strategy.get_best_attack_target(game_state)

            # my_index == -1代表英雄攻击, -2 代表不攻击
            if my_index != -2:
                strategy.my_entity_attack_oppo(game_state, my_index, oppo_index)
            else:
                click.end_turn()
                time.sleep(STATE_CHECK_INTERVAL)

    def QuittingBattle(self):
        self.print_out()
        time.sleep(5)
        loop_count = 0
        while True:
            if quitting_flag:
                sys.exit(0)

            state = get_screen.get_state()
            if state in [FSM_CHOOSING_HERO, FSM_LEAVE_HS]:
                return state
            click.cancel_click()
            click.test_click()
            click.commit_error_report()

            loop_count += 1
            if loop_count >= 15:
                warn_print("QuittingBattle loop_count >= 15")
                return FSM_ERROR

            time.sleep(STATE_CHECK_INTERVAL)

    def GoBackHSAction(self):
        self.print_out()
        time.sleep(3)

        while not get_screen.test_hs_available():
            click.enter_HS()
            time.sleep(10)

        # 有时候炉石进程会直接重写Power.log, 这时应该重新创建文件操作句柄
        self.init()

        return FSM_MAIN_MENU

    def HandleErrorAction(self):
        self.print_out()
        if not get_screen.test_hs_available():
            return FSM_LEAVE_HS
        else:
            click.commit_error_report()
            click.click_setting()
            time.sleep(0.5)
            # 先尝试点认输
            click.left_click(960, 380)
            time.sleep(2)

            get_screen.terminate_HS()
            time.sleep(STATE_CHECK_INTERVAL)

            return FSM_LEAVE_HS

    def FSM_dispatch(self, next_state):
        dispatch_dict = {
            FSM_LEAVE_HS: self.GoBackHSAction,
            FSM_MAIN_MENU: self.MainMenuAction,
            FSM_CHOOSING_HERO: self.ChoosingHeroAction,
            FSM_MATCHING: self.MatchingAction,
            FSM_CHOOSING_CARD: self.ChoosingCardAction,
            FSM_BATTLING: self.Battling,
            FSM_ERROR: self.HandleErrorAction,
            FSM_QUITTING_BATTLE: self.QuittingBattle,
        }

        if next_state not in dispatch_dict:
            error_print("Unknown state!")
            sys.exit()
        else:
            return dispatch_dict[next_state]()

    def print_out(self):
        global time_begin
        global game_count

        sys_print("Enter State " + str(self._fsm_state))

        if self._fsm_state == FSM_LEAVE_HS:
            warn_print("HearthStone not found! Try to go back to HS")

        if self._fsm_state == FSM_CHOOSING_CARD:
            game_count += 1
            sys_print("The " + str(game_count) + " game begins")
            time_begin = time.time()

        if self._fsm_state == FSM_QUITTING_BATTLE:
            sys_print("The " + str(game_count) + " game ends")
            time_now = time.time()
            if time_begin > 0:
                info_print("The last game last for : {} mins {} secs"
                           .format(int((time_now - time_begin) // 60),
                                   int(time_now - time_begin) % 60))

        return

    def init(self):
        global game_state, log_iter
        if GAME_STRATEGY == 0:
            return
        # 有时候炉石退出时python握着Power.log的读锁, 因而炉石无法
        # 删除Power.log. 而当炉石重启时, 炉石会从头开始写Power.log,
        # 但此时python会读入完整的Power.log, 并在原来的末尾等待新的写入. 那
        # 样的话python就一直读不到新的log. 状态机进而卡死在匹配状态(不
        # 知道对战已经开始)
        # 这里是试图在每次初始化文件句柄的时候删除已有的炉石日志. 如果要清空的
        # 日志是关于当前打开的炉石的, 那么炉石会持有此文件的写锁, 使脚本无法
        # 清空日志. 这使得脚本不会清空有意义的日志
        if os.path.exists(HEARTHSTONE_POWER_LOG_PATH):
            try:
                file_handle = open(HEARTHSTONE_POWER_LOG_PATH, "w")
                file_handle.seek(0)
                file_handle.truncate()
                info_print("Success to truncate Power.log")
            except OSError:
                warn_print("Fail to truncate Power.log, maybe someone is using it")
        else:
            info_print("Power.log does not exist")

        game_state = GameState()
        log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
        a_game_state.init()

    def run(self):
        check_name()
        print_info_init()
        self.init()
        keyboard.add_hotkey("ctrl+q", system_exit)
        self.AutoHS_automata()
