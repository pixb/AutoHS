# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 4:51
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : t_game_state.py
# @Software: PyCharm
# @Description:
from hearthstone.enums import GameTag, State

from hslog import LogParser
from hslog.export import EntityTreeExporter

from constants.constants import HEARTHSTONE_POWER_LOG_PATH
from model.t_my_state import t_my_state
from model.t_oppo_state import t_oppo_state


class t_game_state:
    def __init__(self):
        self.parser = None
        self.parse = None
        self.game = None
        self.game_entity_id = 0
        self.player_id_map_dict = {}
        self.my_name = ""
        self.oppo_name = ""
        self.my_player_id = 0
        self.oppo_player_id = 0
        self.entity_dict = {}
        self.current_update_id = 0
        self.my_hero = None
        self.my_state = t_my_state()
        self.oppo_state = t_oppo_state()
        self.init()

    def __str__(self):
        res = \
            f"""t_game_state:
    game_entity_id: {self.game_entity_id}
    my_name: {self.my_name}
    oppo_name: {self.oppo_name}
    my_player_id: {self.my_player_id}
    oppo_player_id: {self.oppo_player_id}
    current_update_id: {self.current_update_id}
    entity_keys: {[list(self.entity_dict.keys())]}

"""
        return res

    def init(self):
        self.parser = LogParser()
        try:
            with open(HEARTHSTONE_POWER_LOG_PATH, "r", encoding="utf8") as f:
                self.parser.read(f)
            self.parser.flush()
            if len(self.parser.games) < 1:
                return False
            packet_tree = self.parser.games[-1]
            exporter = EntityTreeExporter(packet_tree, player_manager=self.parser.player_manager)
            self.game = exporter.export().game
            self.game_entity_id = self.game.id
            self.my_state.init(self.game.players[0])
            self.oppo_state.init(self.game.players[1])
            f.close()
        except:
            return False
        else:
            return True

    @property
    def is_end(self):
        return self.game.tags.get(GameTag.STATE) == State.COMPLETE

    @property
    def game_num_turns_in_play(self):
        if self.game.tags.get(GameTag.NUM_TURNS_IN_PLAY) is None:
            return 0
        else:
            return self.game.tags.get(GameTag.NUM_TURNS_IN_PLAY)

    @property
    def available(self):
        if self.game is None:
            return False
        return self.game_entity_id != 0
