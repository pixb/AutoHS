# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 7:31
# @Author  : pixb
# @Email   : tpxsky@163.com
# @File    : t_my_state.py
# @Software: PyCharm
# @Description: my game state info
from hearthstone.entities import Player
from hearthstone.enums import Zone, CardType, GameTag, PlayState


class t_my_state:
    def __init__(self):
        self.my_hero = None
        self.my_hero_power = None
        self.my_weapon = None
        self.my_total_mana = 0
        self.my_used_mana = 0
        self.my_temp_mana = 0
        self.my_hand_cards = []
        self.my_minions = []
        self.my_graveyard = []
        self.can_use_power = False
        self.player = None

    def init(self, player: Player):
        print("\t ====  t_my_state init()   == \n")
        self.player = player
        self.my_hand_cards.clear()
        self.my_minions.clear()
        self.my_graveyard.clear()
        for et in player.entities:
            if et.zone == Zone.HAND:
                self.my_hand_cards.append(et)
            if et.zone == Zone.PLAY:
                if et.type == CardType.MINION:
                    self.my_minions.append(et)
                if et.type == CardType.HERO:
                    self.my_hero = et
                if et.type == CardType.HERO_POWER:
                    self.my_hero_power = et
                if et.type == CardType.WEAPON:
                    self.my_weapon = et
            if et.zone == Zone.GRAVEYARD:
                self.my_graveyard.append(et)
        self.my_total_mana = player.tags.get(GameTag.RESOURCES)
        self.my_used_mana = player.tags.get(GameTag.RESOURCES_USED)
        self.my_temp_mana = player.tags.get(GameTag.TEMP_RESOURCES)
        self.my_minions.sort(key=lambda temp: temp.tags.get(GameTag.ZONE_POSITION))
        self.my_hand_cards.sort(key=lambda temp: temp.tags.get(GameTag.ZONE_POSITION))
        print("====================hand card count:{}".format(self.my_hand_card_num))

    def update(self, game_state):
        self.my_hand_cards.clear()
        self.my_minions.clear()
        self.my_graveyard.clear()

        for entity in game_state.entity_dict.values():
            if entity.query_tag("ZONE") == "HAND":
                if game_state.is_my_entity(entity):
                    hand_card = entity.corresponding_entity
                    self.my_hand_cards.append(hand_card)

            elif entity.zone == "PLAY":
                if entity.cardtype == "MINION":
                    minion = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_minions.append(minion)

                elif entity.cardtype == "HERO":
                    hero = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_hero = hero

                elif entity.cardtype == "HERO_POWER":
                    hero_power = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_hero_power = hero_power

                elif entity.cardtype == "WEAPON":
                    weapon = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_weapon = weapon

            elif entity.zone == "GRAVEYARD":
                if game_state.is_my_entity(entity):
                    self.my_graveyard.append(entity)

        # 从这里取用户的一些信息
        if game_state.my_entity_id != 0:
            # print("my entity -->{}".format(state.my_entity.query_tag("RESOURCES")))
            self.my_total_mana = int(game_state.my_entity.query_tag("RESOURCES"))
            self.my_used_mana = int(game_state.my_entity.query_tag("RESOURCES_USED"))
            self.my_temp_mana = int(game_state.my_entity.query_tag("TEMP_RESOURCES"))

        self.my_minions.sort(key=lambda temp: temp.zone_pos)
        self.my_hand_cards.sort(key=lambda temp: temp.zone_pos)

    @property
    def my_last_mana(self):
        return self.my_total_mana - self.my_used_mana + self.my_temp_mana

    @property
    def my_hand_card_num(self):
        return len(self.my_hand_cards)

    @property
    def my_minion_num(self):
        return len(self.my_minions)

    @property
    def my_heuristic_value(self):
        total_h_val = self.my_hero.heuristic_val
        if self.my_weapon:
            total_h_val += self.my_weapon.heuristic_val
        for minion in self.my_minions:
            total_h_val += minion.heuristic_val
        return total_h_val

    @property
    def my_detail_hero_power(self):
        return self.my_hero_power.detail_hero_power

    def my_total_spell_power(self):
        return sum([minion.spell_power for minion in self.my_minions])

    @property
    def my_total_attack(self):
        count = 0
        for my_minion in self.my_minions:
            if my_minion.can_beat_face:
                count += my_minion.attack

        if self.my_hero.can_attack:
            count += self.my_hero.attack

        return count

    def is_end_win(self):
        if self.player is None:
            return False
        return self.player.tags.get(GameTag.PLAYSTATE) == PlayState.WON

    @property
    def is_my_turn(self):
        return self.player.tags.get(GameTag.CURRENT_PLAYER) == self.player.player_id

    @property
    def num_turns_in_play(self):
        if self.player.tags.get(GameTag.NUM_TURNS_IN_PLAY) is None:
            return 0
        else:
            return self.player.tags.get(GameTag.NUM_TURNS_IN_PLAY)
