# def MainMenuAction():
#     print_out()
#
#     time.sleep(30)
#
#     while True:
#         click.enter_battle_mode()
#         time.sleep(5)
#
#         state = get_screen.get_state()
#
#         # 重新连接对战之类的
#         if state == FSM_BATTLING:
#             ok = update_game_state()
#             if ok and game_state.available:
#                 return FSM_BATTLING
#         if state == FSM_CHOOSING_HERO:
#             return FSM_CHOOSING_HERO

import time
import sys
import click

if __name__ == "__main__":
   time.sleep(3)
   while True:
       click.enter_battle_mode()
       time.sleep(5)

