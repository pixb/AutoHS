import re

if __name__ == "__main__":
    print("redemo run...")
    log_string="D 05:50:19.2236266 GameState.DebugPrintPower() -     GameEntity EntityID=1"
    # "D 04:23:18.0000001 GameState.DebugPrintPower() -     GameEntity EntityID=1"
    GAME_STATE_PATTERN = re.compile(r"D [\d]{2}:[\d]{2}:[\d]{2}.[\d]{7} GameState.DebugPrint(Game|Power)\(\) - (.+)")
    # `compile` 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象
    # 匹配返回match对象
    match_obj = GAME_STATE_PATTERN.match(log_string)
    print("match_obj:{}".format(match_obj))
    ling_string= match_obj.group(2)
    print("line_string:{}".format(ling_string))

