import time
import random


from spirecomm.spire.game import Game
from spirecomm.spire.character import Intent, PlayerClass
import spirecomm.spire.card
from spirecomm.spire.screen import RestOption
from spirecomm.communication.action import *
from spirecomm.ai.priorities import *
import copy


class Node:
    global_nodes = 0

    def __init__(self, game, prob, deter, card, target):
        self.game = game
        self.probability = prob
        self.children = []
        self.total_nodes = 0

        self.id = Node.global_nodes
        Node.global_nodes = Node.global_nodes + 1

        self.hasChildren = False
        self.deterministic = deter  # 0 for deterministic, 1 for non-deterministic
        self.done = not game.in_combat
        self.static_value = game.evaluate_state()
        self.deep_evaluation = -69
        self.removed = False

        self.card_to_play = card
        self.card_target = target

    def expand(self,turn_stop):

        playable_cards = [card for card in self.game.hand if card.is_playable]

        playable_cards_no_repeats = []
        for p_card in playable_cards:
            append_card = True
            for r_card in playable_cards_no_repeats:
                if r_card.name == p_card.name and r_card.upgrades == p_card.upgrades:
                    append_card = False

            if (append_card):
                playable_cards_no_repeats.append(p_card)

        if len(playable_cards_no_repeats) > 0:
            self.hasChildren = True
            possible_options = []

            for card_to_play in playable_cards_no_repeats:
                if card_to_play.has_target:
                    for target in self.game.monsters:
                        possible_options.append((card_to_play, target))
                else:
                    possible_options.append((card_to_play, None))

            for i in possible_options:
                self.children.append(
                    Node(self.game.predict_state(i[0], i[1]), self.probability, 0, i[0], i[1]))

        else:
            if turn_stop == self.game.turn:
                self.done = True
            else:
                self.hasChildren = True
                self.deterministic = 1
                for state, prob in self.game.predict_states_turn_end():
                    self.children.append(Node(state, self.probability*prob, 0,None,None))

        for i in self.children:
            if not i.game.in_combat:
                i.done = True
            # if turn_stop == i.game.turn:
            #     i.done = True

        return

    def get_deep_evaluation(self):
        if self.deterministic == 0:
            max = -99999999

            if (not self.hasChildren):
                self.deep_evaluation = self.probability*self.static_value
                return self.probability*self.static_value

            for child in self.children:
                new_val = child.get_deep_evaluation()
                if max < new_val:
                    max = new_val

            self.deep_evaluation = max
            return max
        if self.deterministic == 1:
            if (not self.hasChildren):
                self.deep_evaluation = self.probability*self.static_value
                return self.probability*self.static_value

            sum = 0

            for child in self.children:
                new_val = child.get_deep_evaluation()
                sum = sum + new_val

            self.deep_evaluation = sum
            return sum
        print("I am returning -6942042042042 Ertrorrorroo")
        return -694206942069420  # Error. We should never return this value

    def count_tree_nodes(self):
        sum = 0
        for child in self.children:
            sum = sum + 1 + child.count_tree_nodes()
        return sum

    def heavy_prune(self):

        # Prune all but the max child

        if self.deterministic == 0:
            for child in self.children:
                if (child.deep_evaluation < self.deep_evaluation):
                    child.removed = True
                    self.children.remove(child)

                child.heavy_prune()

        if self.deterministic == 1:
            for child in self.children:
                child.heavy_prune()

        if self.id == 0:
            self.total_nodes = self.count_tree_nodes()

        return

    def __str__(self):
        temp = ""

        temp = temp + "id: " + str(self.id) + "\n"
        temp = temp + "hand: " + str([i.name for i in self.game.hand]) + "\n"
        temp = temp + "children: " + str([i.id for i in self.children]) + "\n"
        temp = temp + "health: " + str(self.game.player.current_hp) + "\n"
        if len(self.game.monsters) > 0:
            temp = temp + "monster: " + str(self.game.monsters[0].current_hp) + "\n"
        temp = temp + "value: " + str(self.deep_evaluation) + "\n\n"

        for i in self.children:
            temp = temp + i.__str__()

        return temp


class CoolRadicalAgent:
    def __init__(self, chosen_class=PlayerClass.THE_SILENT):
        self.game = Game()
        self.errors = 0
        self.choose_good_card = False
        self.skipped_cards = False
        self.visited_shop = False
        self.map_route = []
        self.chosen_class = chosen_class
        self.priorities = Priority()
        self.change_class(chosen_class)
        self.headNode = None

    def change_class(self, new_class):
        self.chosen_class = new_class
        if self.chosen_class == PlayerClass.THE_SILENT:
            self.priorities = SilentPriority()
        elif self.chosen_class == PlayerClass.IRONCLAD:
            self.priorities = IroncladPriority()
        elif self.chosen_class == PlayerClass.DEFECT:
            self.priorities = DefectPowerPriority()
        else:
            self.priorities = random.choice(list(PlayerClass))

    def handle_error(self, error):
        raise Exception(error)

    def get_next_action_in_game(self, game_state,debug_mode = False):
        self.game = game_state
        self.game.play_available = False

        for i in game_state.hand:
            if i.is_playable:
                self.game.play_available = True
                break
        
        if(debug_mode):
            print(self.game.play_available)

        # time.sleep(0.07)
        if self.game.choice_available:
            return self.handle_screen()
        if self.game.proceed_available:
            return ProceedAction()
        if self.game.play_available:
            return self.get_play_card_action(debug_mode)
        if self.game.end_available:
            return EndTurnAction()
        if self.game.cancel_available:
            return CancelAction()

    def get_next_action_out_of_game(self):
        return StartGameAction(self.chosen_class)

    def is_monster_attacking(self):
        for monster in self.game.monsters:
            if monster.intent.is_attack() or monster.intent == Intent.NONE:
                return True
        return False

    def get_incoming_damage(self):
        incoming_damage = 0
        for monster in self.game.monsters:
            if not monster.is_gone and not monster.half_dead:
                if monster.move_adjusted_damage is not None:
                    incoming_damage += monster.move_adjusted_damage * monster.move_hits
                elif monster.intent == Intent.NONE:
                    incoming_damage += 5 * self.game.act
        return incoming_damage

    def get_low_hp_target(self):
        available_monsters = [monster for monster in self.game.monsters if monster.current_hp >
                              0 and not monster.half_dead and not monster.is_gone]
        best_monster = min(available_monsters, key=lambda x: x.current_hp)
        return best_monster

    def get_high_hp_target(self):
        available_monsters = [monster for monster in self.game.monsters if monster.current_hp >
                              0 and not monster.half_dead and not monster.is_gone]
        best_monster = max(available_monsters, key=lambda x: x.current_hp)
        return best_monster

    def many_monsters_alive(self):
        available_monsters = [monster for monster in self.game.monsters if monster.current_hp >
                              0 and not monster.half_dead and not monster.is_gone]
        return len(available_monsters) > 1

    def get_play_card_action(self,debug_mode = False):
        Node.global_nodes = 0

        self.headNode = Node(copy.deepcopy(self.game), 1, 0,None,None)
        turn_stop = self.headNode.game.turn +2

        activeNodes = [self.headNode]

        # Only expands nodes that are either this turn or next turn.
        while  len(activeNodes) >= 1:  # len(activeNodes) >= 1: Node.global_nodes < 4000 and
            current = activeNodes.pop(0)

            current.expand(turn_stop)
            for child in current.children:
                self.headNode.total_nodes = self.headNode.total_nodes + 1
                if not child.done:
                    activeNodes.append(child)

        self.headNode.get_deep_evaluation()
        if(debug_mode):
            print(self.headNode.__str__())
            print([(i.deep_evaluation,i.game.player.block,i.game.monsters[0].current_hp,i.deterministic) for i in self.headNode.children])
            print([[(j.deep_evaluation,j.hasChildren,j.game.player.block) for j in i.children] for i in self.headNode.children])
            print([i.card_to_play.name for i in self.headNode.children ])
            print([i.deep_evaluation for i in self.headNode.children ])
            print(Node.global_nodes)
        best_child = max(self.headNode.children, key=lambda p: p.deep_evaluation)

        # print("Best Card to Play: " + best_child.card_to_play.name)
        if best_child.card_to_play.has_target:

            return PlayCardAction(card = best_child.card_to_play,target_monster = best_child.card_target)
        else:

            return PlayCardAction(card=best_child.card_to_play)
        # self.headNode.heavy_prune()

        # while self.headNode.total_nodes < 4000:  # len(activeNodes) >= 1:
        #     current = activeNodes.pop(0)
        #     if (current.removed):
        #         continue

        #     current.expand()

        #     for child in current.children:
        #         self.headNode.total_nodes = self.headNode.total_nodes + 1
        #         if not child.done:
        #             activeNodes.append(child)


    def handle_screen(self):
        if self.game.screen_type == ScreenType.EVENT:
            if self.game.screen.event_id in ["Vampires", "Masked Bandits", "Knowing Skull", "Ghosts", "Liars Game", "Golden Idol", "Drug Dealer", "The Library"]:
                return ChooseAction(len(self.game.screen.options) - 1)
            
            elif self.game.screen.event_id == "Neow Event" and len(self.game.screen.options) == 1:
                return ChooseAction(0)
            elif self.game.screen.event_id == "Neow Event" :
                return ChooseAction(1)
            else:
                return ChooseAction(0)
        elif self.game.screen_type == ScreenType.CHEST:
            return OpenChestAction()
        elif self.game.screen_type == ScreenType.SHOP_ROOM:
            if not self.visited_shop:
                self.visited_shop = True
                return ChooseShopkeeperAction()
            else:
                self.visited_shop = False
                return ProceedAction()
        elif self.game.screen_type == ScreenType.REST:
            return self.choose_rest_option()
        elif self.game.screen_type == ScreenType.CARD_REWARD:
            return self.choose_card_reward()
        elif self.game.screen_type == ScreenType.COMBAT_REWARD:
            for reward_item in self.game.screen.rewards:
                if reward_item.reward_type == RewardType.POTION and self.game.are_potions_full():
                    continue
                elif reward_item.reward_type == RewardType.CARD and self.skipped_cards:
                    continue
                else:
                    return CombatRewardAction(reward_item)
            self.skipped_cards = False
            return ProceedAction()
        elif self.game.screen_type == ScreenType.MAP:
            return self.make_map_choice()
        elif self.game.screen_type == ScreenType.BOSS_REWARD:
            relics = self.game.screen.relics
            best_boss_relic = self.priorities.get_best_boss_relic(relics)
            return BossRewardAction(best_boss_relic)
        elif self.game.screen_type == ScreenType.SHOP_SCREEN:
            if self.game.screen.purge_available and self.game.gold >= self.game.screen.purge_cost:
                return ChooseAction(name="purge")
            for card in self.game.screen.cards:
                if self.game.gold >= card.price and not self.priorities.should_skip(card):
                    return BuyCardAction(card)
            for relic in self.game.screen.relics:
                if self.game.gold >= relic.price:
                    return BuyRelicAction(relic)
            return CancelAction()
        elif self.game.screen_type == ScreenType.GRID:
            if not self.game.choice_available:
                return ProceedAction()
            if self.game.screen.for_upgrade or self.choose_good_card:
                available_cards = self.priorities.get_sorted_cards(
                    self.game.screen.cards)
            else:
                available_cards = self.priorities.get_sorted_cards(
                    self.game.screen.cards, reverse=True)
            num_cards = self.game.screen.num_cards
            return CardSelectAction(available_cards[:num_cards])
        elif self.game.screen_type == ScreenType.HAND_SELECT:
            if not self.game.choice_available:
                return ProceedAction()
            # Usually, we don't want to choose the whole hand for a hand select. 3 seems like a good compromise.
            num_cards = min(self.game.screen.num_cards, 3)
            return CardSelectAction(self.priorities.get_cards_for_action(self.game.current_action, self.game.screen.cards, num_cards))
        else:
            return ProceedAction()

    def choose_rest_option(self):
        rest_options = self.game.screen.rest_options
        if len(rest_options) > 0 and not self.game.screen.has_rested:
            if RestOption.REST in rest_options and self.game.current_hp < self.game.max_hp / 2:
                return RestAction(RestOption.REST)
            elif RestOption.REST in rest_options and self.game.act != 1 and self.game.floor % 17 == 15 and self.game.current_hp < self.game.max_hp * 0.9:
                return RestAction(RestOption.REST)
            elif RestOption.SMITH in rest_options:
                return RestAction(RestOption.SMITH)
            elif RestOption.LIFT in rest_options:
                return RestAction(RestOption.LIFT)
            elif RestOption.DIG in rest_options:
                return RestAction(RestOption.DIG)
            elif RestOption.REST in rest_options and self.game.current_hp < self.game.max_hp:
                return RestAction(RestOption.REST)
            else:
                return ChooseAction(0)
        else:
            return ProceedAction()

    def count_copies_in_deck(self, card):
        count = 0
        for deck_card in self.game.deck:
            if deck_card.card_id == card.card_id:
                count += 1
        return count

    def choose_card_reward(self):
        reward_cards = self.game.screen.cards
        if self.game.screen.can_skip and not self.game.in_combat:
            pickable_cards = [card for card in reward_cards if self.priorities.needs_more_copies(
                card, self.count_copies_in_deck(card))]
        else:
            pickable_cards = reward_cards
        if len(pickable_cards) > 0:
            potential_pick = self.priorities.get_best_card(pickable_cards)
            return CardRewardAction(potential_pick)
        elif self.game.screen.can_bowl:
            return CardRewardAction(bowl=True)
        else:
            self.skipped_cards = True
            return CancelAction()

    def generate_map_route(self):
        node_rewards = self.priorities.MAP_NODE_PRIORITIES.get(self.game.act)
        best_rewards = {0: {
            node.x: node_rewards[node.symbol] for node in self.game.map.nodes[0].values()}}
        best_parents = {
            0: {node.x: 0 for node in self.game.map.nodes[0].values()}}
        min_reward = min(node_rewards.values())
        map_height = max(self.game.map.nodes.keys())
        for y in range(0, map_height):
            best_rewards[y+1] = {node.x: min_reward *
                                 20 for node in self.game.map.nodes[y+1].values()}
            best_parents[y+1] = {node.x: -
                                 1 for node in self.game.map.nodes[y+1].values()}
            for x in best_rewards[y]:
                node = self.game.map.get_node(x, y)
                best_node_reward = best_rewards[y][x]
                for child in node.children:
                    test_child_reward = best_node_reward + \
                        node_rewards[child.symbol]
                    if test_child_reward > best_rewards[y+1][child.x]:
                        best_rewards[y+1][child.x] = test_child_reward
                        best_parents[y+1][child.x] = node.x
        best_path = [0] * (map_height + 1)
        best_path[map_height] = max(
            best_rewards[map_height].keys(), key=lambda x: best_rewards[map_height][x])
        for y in range(map_height, 0, -1):
            best_path[y - 1] = best_parents[y][best_path[y]]
        self.map_route = best_path

    def make_map_choice(self):
        if len(self.game.screen.next_nodes) > 0 and self.game.screen.next_nodes[0].y == 0:
            self.generate_map_route()
            self.game.screen.current_node.y = -1
        if self.game.screen.boss_available:
            return ChooseMapBossAction()
        chosen_x = self.map_route[self.game.screen.current_node.y + 1]
        for choice in self.game.screen.next_nodes:
            if choice.x == chosen_x:
                return ChooseMapNodeAction(choice)
        # This should never happen
        return ChooseAction(0)
