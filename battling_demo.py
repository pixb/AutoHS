"""
对战测试Demo
"""

from update_game_state_demo import  *
from strategy import  *

DEBUG_USE_CARD = True
DEBUG_END_TURN = True

def Battling():
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

    strategy_state = StrategyState(game_state)
    # 考虑要不要出牌
    delta_h, index, args = strategy_state.best_h_index_arg()
    print("put card:\n"
          "\t delta_h:{}\n"
          "\t index:{}\n"
          "\t args:{}\n"
          .format(delta_h, index, args))

    if delta_h > 0 and DEBUG_USE_CARD:
         strategy_state.use_card(index, *args)


    # 考虑要不要用技能
    hero_power = strategy_state.my_detail_hero_power
    if hero_power and strategy_state.my_last_mana >= 2:
        delta_h, *args = hero_power.best_h_and_arg(strategy_state, -1)
        debug_print(str(delta_h) + str(args))
        if delta_h > 0:
            hero_power.use_with_arg(strategy_state, -1, *args)

    print("power:\n"
          "\t hero_power:{}"
          .format(hero_power))
    # if DEBUG_END_TURN:
    #     click.end_turn()


if __name__ == "__main__":
    Battling()

