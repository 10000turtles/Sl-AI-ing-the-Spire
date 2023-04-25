from enum import Enum

import spirecomm.spire.relic
import spirecomm.spire.card
import spirecomm.spire.character
import spirecomm.spire.map
import spirecomm.spire.potion
import spirecomm.spire.screen
# Intent, PlayerClass, Power,Monster_Action,Monster_Move
from spirecomm.spire.character import *
import copy
import itertools as it
import math
import random
import json


class RoomPhase(Enum):
    COMBAT = 1,
    EVENT = 2,
    COMPLETE = 3,
    INCOMPLETE = 4


class Game:
    global_json_counter = 0

    def __init__(self):

        # General state

        self.current_action = None
        self.current_hp = 0
        self.max_hp = 0
        self.floor = 0
        self.act = 0
        self.gold = 0
        self.seed = 0
        self.character = None
        self.ascension_level = None
        self.relics = []
        self.deck = []
        self.potions = []
        self.map = []

        # Combat state

        self.in_combat = False
        self.player = None
        self.monsters = []
        self.draw_pile = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.hand = []
        self.limbo = []
        self.card_in_play = None
        self.turn = 0
        self.cards_discarded_this_turn = 0

        # Current Screen

        self.screen = None
        self.screen_up = False
        self.screen_type = None
        self.room_phase = None
        self.room_type = None
        self.choice_list = []
        self.choice_available = False

        # Available Commands

        self.end_available = False
        self.potion_available = False
        self.play_available = False
        self.proceed_available = False
        self.cancel_available = False

        # Evaluation

        self.value = 0

    @classmethod
    def from_json(cls, json_state, available_commands, raw_data):
        game = cls()
        game.current_action = json_state.get("current_action", None)
        game.current_hp = json_state.get("current_hp")
        game.max_hp = json_state.get("max_hp")
        game.floor = json_state.get("floor")
        game.act = json_state.get("act")
        game.gold = json_state.get("gold")
        game.seed = json_state.get("seed")
        game.character = spirecomm.spire.character.PlayerClass[json_state.get(
            "class")]
        game.ascension_level = json_state.get("ascension_level")
        game.relics = [spirecomm.spire.relic.Relic.from_json(
            json_relic) for json_relic in json_state.get("relics")]
        game.deck = [spirecomm.spire.card.Card.from_json(
            json_card) for json_card in json_state.get("deck")]
        game.map = spirecomm.spire.map.Map.from_json(json_state.get("map"))
        game.potions = [spirecomm.spire.potion.Potion.from_json(
            potion) for potion in json_state.get("potions")]
        game.act_boss = json_state.get("act_boss", None)

        # Screen State

        game.screen_up = json_state.get("is_screen_up", False)
        game.screen_type = spirecomm.spire.screen.ScreenType[json_state.get(
            "screen_type")]
        game.screen = spirecomm.spire.screen.screen_from_json(
            game.screen_type, json_state.get("screen_state"))
        game.room_phase = RoomPhase[json_state.get("room_phase")]
        game.room_type = json_state.get("room_type")
        game.choice_available = "choice_list" in json_state
        if game.choice_available:
            game.choice_list = json_state.get("choice_list")

        # Combat state

        game.in_combat = game.room_phase == RoomPhase.COMBAT
        if game.in_combat:
            combat_state = json_state.get("combat_state")
            game.player = spirecomm.spire.character.Player.from_json(
                combat_state.get("player"))
            game.monsters = [spirecomm.spire.character.Monster.from_json(
                json_monster) for json_monster in combat_state.get("monsters")]
            for i, monster in enumerate(game.monsters):
                monster.monster_index = i
            game.draw_pile = [spirecomm.spire.card.Card.from_json(
                json_card) for json_card in combat_state.get("draw_pile")]
            game.discard_pile = [spirecomm.spire.card.Card.from_json(
                json_card) for json_card in combat_state.get("discard_pile")]
            game.exhaust_pile = [spirecomm.spire.card.Card.from_json(
                json_card) for json_card in combat_state.get("exhaust_pile")]
            game.hand = [spirecomm.spire.card.Card.from_json(
                json_card) for json_card in combat_state.get("hand")]
            game.limbo = [spirecomm.spire.card.Card.from_json(
                json_card) for json_card in combat_state.get("limbo", [])]
            game.card_in_play = combat_state.get("card_in_play", None)
            if game.card_in_play is not None:
                game.card_in_play = spirecomm.spire.card.Card.from_json(
                    game.card_in_play)
            game.turn = combat_state.get("turn", 0)
            game.cards_discarded_this_turn = combat_state.get(
                "cards_discarded_this_turn", 0)

        # Available Commands

        game.end_available = "end" in available_commands
        game.potion_available = "potion" in available_commands
        game.play_available = "play" in available_commands
        game.proceed_available = "proceed" in available_commands or "confirm" in available_commands
        game.cancel_available = "cancel" in available_commands or "leave" in available_commands \
                                or "return" in available_commands or "skip" in available_commands

        try:
            for monster in game.monsters:
                with open(f"json_fight_data/monster_move_ids", "a") as f_write:
                    with open(f"json_fight_data/monster_move_ids", "r") as f_read:
                        if not f"{monster.name}: {monster.intent}" in f_read.read().rstrip():
                            f_write.write(
                                f"{monster.name}: {monster.intent} has id of {monster.move_id}\n")
        except:
            for monster in game.monsters:
                with open(f"C:\\Users\\TheFifthTurtle\\Documents\\GitHub\\Sl-AI-ing-the-Spire\\spirecomm\\json_fight_data\\monster_move_ids", "a") as f_write:
                    with open(f"C:\\Users\\TheFifthTurtle\\Documents\\GitHub\\Sl-AI-ing-the-Spire\\spirecomm\\json_fight_data\\monster_move_ids", "r") as f_read:
                        if not f"{monster.name}: {monster.intent} with damage {monster.move_base_damage}" in f_read.read().rstrip():
                            f_write.write(
                                f"{monster.name}: {monster.intent} with damage {monster.move_base_damage} has id of {monster.move_id}\n")
        # try:
        #   with open(f"json_fight_data/floor_{str(game.floor)}_turn_{str(game.turn)}_action_{str(Game.global_json_counter)}.json", 'w') as f:
        #     Game.global_json_counter = Game.global_json_counter + 1
        #     json.dump(raw_data, f)
        # except:
        #   with open(f"C:\\Users\\TheFifthTurtle\\Documents\\GitHub\\Sl-AI-ing-the-Spire\\spirecomm\\json_fight_data\\floor_{str(game.floor)}_turn_{str(game.turn)}_action_{str(Game.global_json_counter)}.json", 'w') as f:
        #     Game.global_json_counter = Game.global_json_counter + 1
        #     json.dump(raw_data, f)

        return game

    def are_potions_full(self):
        for potion in self.potions:
            if potion.potion_id == "Potion Slot":
                return False
        return True

    def get_real_potions(self):
        potions = []
        for potion in self.potions:
            if potion.potion_id != "Potion Slot":
                potions.append(potion)
        return potions

    def get_incoming_damage(self):
        incoming_damage = 0
        for monster in self.monsters:
            if not monster.is_gone and not monster.half_dead:
                if monster.move_adjusted_damage is not None:
                    incoming_damage += monster.move_adjusted_damage * monster.move_hits
                elif monster.intent == Intent.NONE:
                    incoming_damage += 5 * self.act
        return incoming_damage

    def update_monsters(self):
        for target in self.monsters:
            if (target.current_hp <= 0):
                target.is_gone = True
                self.monsters.remove(target)

            if (len(self.monsters) == 0):
                self.in_combat = False

    def update_cards(self):
        for card in self.hand:
            card.is_playable = True
            if self.player.energy < card.cost:
                card.is_playable = False

    def update(self):
        self.update_monsters()
        self.update_cards()

    def execute_monster_attacks(self):

        # update monsters and add block + power stuff to update_monsters

        for monster in self.monsters:
            monster.block = 0
            monster.move.execute_move(self, monster, self.player)

    def predict_state(self, card, target, node):
        new_game = copy.deepcopy(self)

        if (not target == None):
            for monster in new_game.monsters:
                if target.__eq__(monster):
                    target = monster
                    break

        player_move = Move(*Move.monster_move_data[(card.name, 0)])
        new_game.player.energy -= card.cost
        player_move.execute_move(new_game, new_game.player, target, node, card)
        new_game.update()

        return new_game

    def predict_states_turn_end(self):

        new_games = []

        new_game_template = copy.deepcopy(self)
        new_game_template.turn = new_game_template.turn + 1

        new_game_template.discard_pile.extend(new_game_template.hand)
        new_game_template.hand = []

        new_game_template.execute_monster_attacks()
        new_game_template.player.block = 0

        possible_monster_intents = []

        for monster in new_game_template.monsters:
            possible_monster_intents.append(
                monster.possible_intents(new_game_template))

        for combo in it.product(*possible_monster_intents):
            count = 0
            temp_game = copy.deepcopy(new_game_template)
            if (len(temp_game.draw_pile) >= 5):
                possible_hands = it.combinations(
                    temp_game.draw_pile, 5)
            else:
                temp_game.hand.extend(temp_game.draw_pile)
                temp_game.draw_pile.extend(temp_game.discard_pile)
                temp_game.discard_pile = []

                possible_hands = it.combinations(
                    temp_game.draw_pile, 5-len(temp_game.hand))

            for hand in possible_hands:
                hand = list(hand)

                original_hand = copy.deepcopy(temp_game.hand)
                count = count + 1

                # temp_game = copy.deepcopy(new_game_template)
                # print("hand: " + str(hand))
                if len(temp_game.hand) == 0:
                    temp_game.hand = hand
                else:
                    temp_game.hand.extend(hand)

                # Add exhaust mechanics here
                # Add "on draw" mechanics here
                # Add max hand size here
                # OMG wtf this is complex

                for i in range(len(temp_game.monsters)):
                    temp_game.monsters[i].second_last_move_id = temp_game.monsters[i].last_move_id
                    temp_game.monsters[i].last_move_id = temp_game.monsters[i].move_id
                    temp_game.monsters[i].move_id = combo[i].intent

                temp_game.player.energy = 3
                temp_game.update()

                new_games.append(
                    (temp_game, math.prod([i.probability for i in combo])))

                temp_game.hand = original_hand

        max_game_sample = 400
        if len(new_games) > max_game_sample:
            count = max_game_sample
            new_games = random.sample(new_games, max_game_sample)

        for i in range(len(new_games)):
            # Tuples dont support item assignment so I have to do it this way
            new_games[i] = (new_games[i][0], new_games[i][1]*(1/count))

        # Calculate Probabilities (And set non-deterministic)
        return new_games

    def predict_card_draw(self, cards):
        new_games = []

        new_game_template = copy.deepcopy(self)

        if (len(new_game_template.draw_pile) >= cards):
            possible_hands = it.combinations(
                new_game_template.draw_pile, cards)
        else:
            new_cards_to_draw = cards - len(new_game_template.draw_pile)
            new_game_template.hand.extend(new_game_template.draw_pile)
            new_game_template.draw_pile.extend(new_game_template.discard_pile)
            new_game_template.discard_pile = []

            possible_hands = it.combinations(self.draw_pile, new_cards_to_draw)

        count = 0
        for hand in possible_hands:
            count = count + 1
            temp_game = copy.deepcopy(new_game_template)
            hand = list(hand)

            temp_game.hand.extend(hand)

            for i in hand:
                temp_game.draw_pile.remove(i)

            new_games.append((temp_game, 1))

        for i in range(len(new_games)):
            new_games[i] = (new_games[i][0], new_games[i][1]*(1/count))

        return new_games

    def evaluate_state(self):

        game_state = copy.deepcopy(self)
        game_state.execute_monster_attacks()
        value = 0

        value = value + 3*game_state.player.current_hp
        if "Gremlin Nob" in [monster.name for monster in game_state.monsters]:
            value = value - 10*sum([i.current_hp for i in game_state.monsters])
        else:
            value = value - sum([i.current_hp for i in game_state.monsters])

        if (game_state.player.current_hp <= 0):
            value = -999  # Might need to change to a lower number.

        # We still need to add more evaluation here (potions, max hp, status effects, etc)
        self.value = value
        return self.value
