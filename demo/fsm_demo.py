from typing import Any
import sys
import keyboard

quitting_flag  = False

FSM_state = ""
STATE_A = "a"
STATE_B = "b"
STATE_C = "c"

def system_exit():
    global quitting_flag

    sys_print(f"一共完成了{game_count}场对战, 赢了{win_count}场")
    print_info_close()
    quitting_flag = True

    sys.exit(0)

def get_state():
    return STATE_A

def autorun():
    print("autorun()...")
    global FSM_state
    while 1:
        if quitting_flag:
            sys.exit(0)

        if FSM_state == "":
            FSM_state = get_state()
        FSM_state = FSM_dispatch(FSM_state)

def a():
    print("a state run...")

def b():
    print("a state run...")

def c():
    print("c state run...")

def FSM_dispatch(next_state):
    print("FSM_dispatch()--->next_state:{}".format(next_state))
    dispatch_dict = {
        STATE_A: a,
        STATE_B: b,
        STATE_C: c,
    }

    if next_state not in dispatch_dict:
        print("Unknown state!")
        sys.exit()
    else:
        return dispatch_dict[next_state]()


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", system_exit)
    autorun()
