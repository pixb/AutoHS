from strategy import *

"""
这个Demo用来调试读取Power.log，并完成解析初始化游戏状态的过程
"""
if __name__ == "__main__":
    log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
    state = GameState()
    DEBUG_PRINT = 1

    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        sys_print("未找到Power.log，请启动炉石并开始对战")
        sys.exit(-1)

    for x in log_container.message_list:
        update_state(state, x)

    with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
        f.write(str(state))

    print("game_state.my_entity:{}".format(state.my_entity))

    strategy_state = StrategyState(state)
