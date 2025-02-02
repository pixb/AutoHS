import win32gui
import win32con
import time
from pynput.mouse import Button, Controller
import random
import sys

from utils.print_info import *


def click_button(x, y, button):
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    mouse = Controller()
    time.sleep(0.1)
    mouse.position = (x, y)
    time.sleep(0.1)
    mouse.press(button)
    time.sleep(0.1)
    mouse.release(button)


def left_click(x, y):
    click_button(x, y, Button.left)


def right_click(x, y):
    click_button(x, y, Button.right)


def choose_my_minion(mine_index, mine_num):
    time.sleep(OPERATE_INTERVAL)
    x = 960 - (mine_num - 1) * 70 + mine_index * 140
    y = 600
    left_click(x, y)


def choose_my_hero():
    time.sleep(OPERATE_INTERVAL)
    left_click(960, 850)


def choose_opponent_minion(oppo_index, oppo_num):
    time.sleep(OPERATE_INTERVAL)
    x = 960 - (oppo_num - 1) * 70 + oppo_index * 140
    y = 400
    left_click(x, y)


def choose_oppo_hero():
    time.sleep(OPERATE_INTERVAL)
    left_click(960, 200)


def cancel_click():
    time.sleep(TINY_OPERATE_INTERVAL)
    right_click(50, 400)


def test_click():
    time.sleep(TINY_OPERATE_INTERVAL)
    left_click(50, 400)


HAND_CARD_X = [
    [],  # 0
    [885],  # 1
    [820, 980],  # 2
    [750, 890, 1040],  # 3
    [690, 820, 970, 1130],  # 4
    [680, 780, 890, 1010, 1130],  # 5
    [660, 750, 840, 930, 1020, 1110],  # 6
    [660, 733, 810, 885, 965, 1040, 1120],  # 7
    [650, 720, 785, 855, 925, 995, 1060, 1130],  # 8
    [650, 710, 765, 825, 880, 950, 1010, 1070, 1140],  # 9
    [647, 700, 750, 800, 860, 910, 970, 1020, 1070, 1120]  # 10
]


def choose_card(card_index, card_num):
    time.sleep(OPERATE_INTERVAL)

    assert 0 <= card_index < card_num <= 10
    # x = START[card_num] + 65 + STEP[card_num] * card_index
    x = HAND_CARD_X[card_num][card_index]

    y = 1000
    left_click(x, y)


STARTING_CARD_X = {
    3: [600, 960, 1320],
    5: [600, 850, 1100, 1350],
}


def replace_starting_card(card_index, hand_card_num):
    assert hand_card_num in STARTING_CARD_X
    assert card_index < len(STARTING_CARD_X[hand_card_num])

    time.sleep(OPERATE_INTERVAL)
    left_click(STARTING_CARD_X[hand_card_num][card_index], 500)


def click_middle():
    time.sleep(OPERATE_INTERVAL)
    left_click(960, 500)


def click_setting():
    time.sleep(OPERATE_INTERVAL)
    left_click(1880, 1050)


def choose_and_use_spell(card_index, card_num):
    choose_card(card_index, card_num)
    click_middle()


# 第[i]个随从左边那个空隙记为第[i]个gap
def put_minion(gap_index, minion_num):
    time.sleep(OPERATE_INTERVAL)

    if minion_num >= 7:
        warn_print(f"Try to put a minion but there has already been {minion_num} minions")

    x = 960 - (minion_num - 1) * 70 + 140 * gap_index - 70
    y = 600
    left_click(x, y)


def match_opponent():
    # 一些奇怪的错误提示
    commit_error_report()
    time.sleep(OPERATE_INTERVAL)
    left_click(1400, 900)


def enter_battle_mode():
    # 一些奇怪的错误提示
    commit_error_report()
    time.sleep(OPERATE_INTERVAL)
    left_click(950, 320)


def commit_choose_card():
    time.sleep(OPERATE_INTERVAL)
    left_click(960, 850)


def end_turn():
    time.sleep(OPERATE_INTERVAL)
    left_click(1550, 500)


def commit_error_report():
    # 一些奇怪的错误提示
    left_click(1100, 820)
    # 如果已断线, 点这里时取消
    left_click(960, 650)


def emoj(target=None):
    emoj_list = [(800, 880), (800, 780), (800, 680), (1150, 680), (1150, 780)]
    right_click(960, 830)
    time.sleep(OPERATE_INTERVAL)

    if target is None:
        x, y = emoj_list[random.randint(1, 4)]
    else:
        x, y = emoj_list[target]
    left_click(x, y)
    time.sleep(OPERATE_INTERVAL)


def click_skill():
    time.sleep(OPERATE_INTERVAL)
    left_click(1150, 850)


def use_skill_no_point():
    click_skill()
    cancel_click()


def use_skill_point_mine(my_index, my_num):
    click_skill()

    if my_index < 0:
        choose_my_hero()
    else:
        choose_my_minion(my_index, my_num)

    cancel_click()


def minion_beat_minion(mine_index, mine_number, oppo_index, oppo_num):
    choose_my_minion(mine_index, mine_number)
    choose_opponent_minion(oppo_index, oppo_num)
    cancel_click()


def minion_beat_hero(mine_index, mine_number):
    choose_my_minion(mine_index, mine_number)
    choose_oppo_hero()
    cancel_click()


def hero_beat_minion(oppo_index, oppo_num):
    choose_my_hero()
    choose_opponent_minion(oppo_index, oppo_num)
    cancel_click()


def hero_beat_hero():
    choose_my_hero()
    choose_oppo_hero()
    cancel_click()


def enter_HS():
    hwnd = win32gui.FindWindow(None, "战网")

    if hwnd == 0:
        error_print("未找到应用战网")
        sys.exit()

    # left_click(180, 910)
    # 把战网客户端拉回前台以便点击
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        warn_print("Error while trying to move BattleNet foreground")

    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
    time.sleep(1)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    left_click(left + 180, bottom - 110)


if __name__ == "__main__":
    emoj(0)
