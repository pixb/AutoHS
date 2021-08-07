"""
更新游戏状态Demo
为了单独测试更新游戏状态所以做了肢解
"""

from game_state import *

game_state = GameState()
log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)

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

    return True


if __name__ == "__main__":
    ok = update_game_state()
    print("update_game_state()={}".format(ok))
