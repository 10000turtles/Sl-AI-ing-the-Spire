from enum import Enum
import random
import copy

from spirecomm.spire.power import Power
# from spirecomm.spire.game import Game
from spirecomm.spire.card import Card

import math
from spirecomm.spire.card import CardType


class Intent(Enum):
    ATTACK = 1
    ATTACK_BUFF = 2
    ATTACK_DEBUFF = 3
    ATTACK_DEFEND = 4
    BUFF = 5
    DEBUFF = 6
    STRONG_DEBUFF = 7
    DEBUG = 8
    DEFEND = 9
    DEFEND_DEBUFF = 10
    DEFEND_BUFF = 11
    ESCAPE = 12
    MAGIC = 13
    NONE = 14
    SLEEP = 15
    STUN = 16
    UNKNOWN = 17

    def is_attack(self):
        return self in [Intent.ATTACK, Intent.ATTACK_BUFF, Intent.ATTACK_DEBUFF, Intent.ATTACK_DEFEND]


class Monster_Action:

    # format: monster: {movename1: move_id1, movename2: move_id2}
    id_map = {
        "Jaw Worm": {"Chomp": 1, "Bellow": 2, "Thrash": 3},
        "FuzzyLouseNormal": {"Bite": 3, "Grow": 4},
        "FuzzyLouseDefensive": {"Bite": 3, "Spit Web": 4},
        "Cultist": {"Incantation": 3, "Dark Strike": 1},
        "Acid Slime (M)": {"Corrosive Spit": 1, "Lick": 4, "Tackle": 2},
        "Acid Slime (L)": {"Corrosive Spit": 1, "Lick": 4, "Tackle": 2, "Split": 3},
        "Spike Slime (M)": {"Flame Tackle": 1, "Lick": 4},
        "Spike Slime (L)": {"Flame Tackle": 1, "Lick": 4, "Split": 3},
        "Acid Slime (S)": {"Lick": 1, "Tackle": 2},
        "Spike Slime (S)": {"Tackle": 1},
        "Looter": {"Mug": 1,  "Lunge": 4, "Smoke Bomb": 2, "Escape": 3},
        "Fungi Beast": {"Bite": 1, "Grow": 2},
        "Hexaghost": {"Activate": 5, "Divider": 1, "Inferno": 6, "Sear": 4, "Tackle": 2, "Inflame": 3},
        "Slime Boss": {"Goop Spray": 4, "Preparing": 2, "Slam": 1, "Split": 3},
        "The Guardian": {"Charging Up": 6, "Fierce Bash": 2, "Vent Steam": 7, "Whirlwind": 5, "Defensive Mode": 1, "Roll Attack": 3, "Twin Slam": 4},
        "Gremlin Nob": {"Bellow": 3, "Rush": 1, "Skull Bash": 2},
        "Sentry": {"Beam": 4, "Bolt": 3},
        "Lagavulin": {"Sleep": 5, "Stun": 4, "Attack": 3, "Siphon Soul": 1},
        "SlaverBlue": {"Stab": 1, "Rake": 4},
        "SlaverRed": {"Stab": 1, "Scrape": 3, "Entangle": 2},
        "Fat Gremlin": {"Smash": 2},
        "Mad Gremlin": {"Scratch": 1},
        "Shield Gremlin": {"Protect": 1, "Shield Bash": 2},
        "Sneaky Gremlin": {"Puncture": 1},
        "Gremlin Wizard": {"Charging": 2, "Ultimate Blast": 1},

        "Shelled Parasite": {"Double Strike": 2, "Suck": 3, "Fell": 1},
        "Spheric Guardian": {"Slam": 1, "Activate": 2, "Harden": 3, "Attack/Debuff": 4},
        "Centurion": {"Slash": 1, "Fury": 3, "Defend": 2},
        "Mystic": {"Heal": 2, "Buff": 3, "Attack/Debuff": 1},
        "Snake Plant": {"Chomp": 1, "Enfeebling Spores": 2},
        "Snecko": {"Perplexing Glare": 1, "Tail Whip": 3, "Bite": 2},
        "Byrd": {"Caw": 6, "Stun": 4, "Peck": 1, "Swoop": 3, "Fly": 2, "Headbutt": 5},
        "Chosen": {"Poke": 5, "Zap": 1, "Debilitate": 3, "Drain": 2, "Hex": 4},
        "Mugger": {"Mug": 1,  "Lunge": 4, "Smoke Bomb": 2, "Escape": 3},
        "Book of Stabbing": {"Multi-Stab": 1, "Single Stab": 2},
        "Pointy": {"Attack": 1},
        "Romeo": {"Mock": 2, "Agonizing Slash": 3, "Cross Slash": 1},
        "Bear": {"Bear Hug": 2, "Lunge": 3, "Maul": 1},
        "Gremlin Leader": {"Encourage": 3, "Rally!": 2, "Stab": 4},
        "Taskmaster": {"Scouring Whip": 2},
        "Bronze Automaton": {"Spawn Orbs": 4, "Boost": 5, "Flail": 1, "HYPER BEAM": 2, "Stun": 3},
        "Orb": {"Stasis": 3, "Beam": 1, "Support Beam": 2},
        "The Champ": {"Execute": 3, "Heavy Slash": 1, "Defensive Stance": 2, "Face Slap": 4, "Taunt": 6, "Gloat": 7, "Anger": 5},
        "The Collector": {"Buff": 3, "Fireball": 2, "Mega Debuff": 4, "Spawn": 1, "Spawn": 5},
        "Torch Head": {"Tackle": 1},

        "Darkling": {"Nip": 3, "Chomp": 1, "Harden": 2, "Reincarnate": 5, "Regrow": 4},
        "Orb Walker": {"Laser": 1, "Claw": 2},
        "Spiker": {"Cut": 1, "Spike": 2},
        "Exploder": {"Slam": 1, "Explode": 2},
        "Repulsor": {"Bash": 2, "Repulse": 1},
        "The Maw": {"Roar": 2, "Drool": 4, "Slam": 3, "Nom": 5},
        "Spire Growth": {"Quick Tackle": 1, "Smash": 3, "Constrict": 2},
        "Transient": {"Attack": 1},
        "Writhing Mass": {"Implant": 4, "Flail": 2, "Wither": 3, "Multi-Strike": 1, "Strong Strike": 0},
        "Giant Head": {"Count": 3, "Glare": 1, "It Is Time": 2},
        "Nemesis": {"Debuff": 4, "Attack": 2, "Scythe": 3},
        "Reptomancer": {"Summon": 2, "Snake Strike": 1, "Big Bite": 3},
        "Dagger": {"Stab": 1, "Explode": 2},
        "Awakened One": {"Slash": 1, "Soul Strike": 2, "Rebirth": 3, "Dark Echo": 5, "Sludge": 6, "Tackle": 8},
        "Donu": {"Circle of Power": 2, "Beam": 0},
        "Deca": {"Square of Protection": 2, "Beam": 0},
        "Time Eater": {"Reverberate": 2, "Head Slam": 4, "Ripple": 3, "Haste": 5}
    }

    def __init__(self, intent, power, probability):

        self.intent = intent
        self.power = power
        self.probability = probability


class PlayerClass(Enum):
    IRONCLAD = 1
    THE_SILENT = 2
    DEFECT = 3


class Orb:

    def __init__(self, name, orb_id, evoke_amount, passive_amount):
        self.name = name
        self.orb_id = orb_id
        self.evoke_amount = evoke_amount
        self.passive_amount = passive_amount

    @classmethod
    def from_json(cls, json_object):
        name = json_object.get("name")
        orb_id = json_object.get("id")
        evoke_amount = json_object.get("evoke_amount")
        passive_amount = json_object.get("passive_amount")
        orb = Orb(name, orb_id, evoke_amount, passive_amount)
        return orb


class Character:

    def __init__(self, max_hp, current_hp=None, block=0):
        self.max_hp = max_hp
        self.current_hp = current_hp
        if self.current_hp is None:
            self.current_hp = self.max_hp
        self.block = block
        self.powers = []

    def adjust_damage(self, base_power, target_powers, heavy_blade=1):
        modified_power = 0

        try:
            index = [i.power_name for i in self.powers].index("Strength")

            modified_power = base_power + self.powers[index].amount*heavy_blade
        except ValueError:
            modified_power = base_power

        try:
            index = [i.power_name for i in self.powers].index("Weakness")

            modified_power = math.floor(modified_power*0.75)
        except ValueError:
            modified_power = modified_power

        try:
            index = [i.power_name for i in target_powers].index("Vulnerable")
            modified_power = math.floor(modified_power*1.5)
        except ValueError:
            modified_power = modified_power

        return modified_power
    # def is_attacked(self):

    def recieve_damage(self, game_state, damage, can_be_blocked):
        try:
            index = [i.power_name for i in self.powers].index("Buffer")
            if (self.powers[index].amount > 0):
                self.powers[index].amount = self.powers[index].amount - 1
                return
        except ValueError:
            pass

        try:
            index = [i.power_name for i in self.powers].index("Intangible")
            if (self.powers[index].amount > 0):
                damage = 1
                return
        except ValueError:
            pass

        try:
            index = [i.power_name for i in self.powers].index("Flying")
            if (self.powers[index].amount > 0):
                damage = math.floor(damage/2)
            self.powers[index].amount = self.powers[index].amount - 1

        except ValueError:
            pass

        took_hp_damage = False
        hp_damage_taken = 0

        if can_be_blocked:
            if self.block < damage:
                self.current_hp = self.current_hp - (damage - self.block)
                hp_damage_taken = hp_damage_taken + (damage - self.block)
                self.block = 0
                took_hp_damage = True

            else:
                self.block = self.block - damage

        else:
            self.current_hp = self.current_hp - damage
            hp_damage_taken = damage
            took_hp_damage = True

        if took_hp_damage:
            try:
                index = [i.power_name for i in self.powers].index(
                    "Plated Armor")
                if (self.powers[index].amount > 0):
                    self.powers[index].amount = self.powers[index].amount - 1

            except ValueError:
                pass

            bfbs = [i for i in [item for sublist in [game_state.discard_pile, game_state.hand, game_state.draw_pile]
                                for item in sublist] if i.name == "Blood for Blood" or i.name == "Blood for Blood+"]
            for i in bfbs:
                i.cost = i.cost - 1

            try:
                index = [i.power_name for i in self.powers].index("Angry")
                try:
                    index2 = [i.power_name for i in self.powers].index(
                        "Strength")
                    self.powers[index2].amount = self.powers[index2].amount + \
                        self.powers[index].amount

                except ValueError:
                    self.powers.append(
                        Power("Strength", "Strength", self.powers[index].amount))

            except ValueError:
                pass

            try:
                index = [i.power_name for i in self.powers].index("Curl Up")

                self.block = self.block + self.powers[index].amount
                del self.powers[index]

            except ValueError:
                pass

            try:
                index = [i.power_name for i in self.powers].index("Malleable")

                self.block = self.block + self.powers[index].amount
                self.powers[index].amount = self.powers[index].amount + 1

            except ValueError:
                pass

            try:
                index = [i.power_name for i in self.powers].index("Mode Shift")

                self.powers[index].amount = self.powers[index].amount - \
                    hp_damage_taken

            except ValueError:
                pass


class Player(Character):

    def __init__(self, max_hp, current_hp=None, block=0, energy=0):
        super().__init__(max_hp, current_hp, block)
        self.name = "Ironclad"
        self.energy = energy
        self.orbs = []

    @classmethod
    def from_json(cls, json_object):
        player = cls(json_object["max_hp"], json_object["current_hp"],
                     json_object["block"], json_object["energy"])
        player.powers = [Power.from_json(json_power)
                         for json_power in json_object["powers"]]
        player.orbs = [Orb.from_json(orb) for orb in json_object["orbs"]]
        return player


class Monster(Character):
    guardian_shifts = 0

    def __init__(self, name, monster_id, max_hp, current_hp, block, intent, half_dead, is_gone, move_id=-1, last_move_id=None, second_last_move_id=None, move_base_damage=0, move_adjusted_damage=0, move_hits=0):
        super().__init__(max_hp, current_hp, block)
        self.name = name
        self.monster_id = monster_id
        self.intent = intent
        self.half_dead = half_dead
        self.is_gone = is_gone
        self.move_id = move_id
        self.last_move_id = last_move_id
        self.second_last_move_id = second_last_move_id
        self.move_base_damage = move_base_damage
        self.move_adjusted_damage = move_adjusted_damage
        self.move_hits = move_hits
        self.monster_index = 0
        if (self.name == "Louse" or self.name == "Slaver"):
            self.move = Move(
                *Move.monster_move_data[(self.monster_id, self.move_id)])
        else:
            self.move = Move(
                *Move.monster_move_data[(self.name, self.move_id)])

    @classmethod
    def from_json(cls, json_object):
        name = json_object["name"]
        monster_id = json_object["id"]
        max_hp = json_object["max_hp"]
        current_hp = json_object["current_hp"]
        block = json_object["block"]
        intent = Intent[json_object["intent"]]
        half_dead = json_object["half_dead"]
        is_gone = json_object["is_gone"]
        move_id = json_object.get("move_id", -1)
        last_move_id = json_object.get("last_move_id", None)
        second_last_move_id = json_object.get("second_last_move_id", None)
        move_base_damage = json_object.get("move_base_damage", 0)
        move_adjusted_damage = json_object.get("move_adjusted_damage", 0)
        move_hits = json_object.get("move_hits", 0)
        monster = cls(name, monster_id, max_hp, current_hp, block, intent, half_dead, is_gone, move_id,
                      last_move_id, second_last_move_id, move_base_damage, move_adjusted_damage, move_hits)
        monster.powers = [Power.from_json(json_power)
                          for json_power in json_object["powers"]]
        return monster

    def possible_intents(self, game_state):

        intents = []
        if self.name == "Jaw Worm":
            chomp = Monster_Action.id_map[self.name]["Chomp"]
            bellow = Monster_Action.id_map[self.name]["Bellow"]
            thrash = Monster_Action.id_map[self.name]["Thrash"]

            if self.last_move_id == bellow:
                intents.append(Monster_Action(chomp, 11, 5/11))
                intents.append(Monster_Action(thrash, 7, 6/11))

            elif self.last_move_id == thrash and self.second_last_move_id == thrash:
                intents.append(Monster_Action(chomp, 11, 5/14))
                intents.append(Monster_Action(bellow, 3, 9/14))

            elif self.last_move_id == chomp:
                intents.append(Monster_Action(bellow, 3, 3/5))
                intents.append(Monster_Action(thrash, 7, 2/5))

            else:
                intents.append(Monster_Action(bellow, 3, 9/20))
                intents.append(Monster_Action(thrash, 7, 6/20))
                intents.append(Monster_Action(chomp, 11, 5/20))

        elif self.name == "Cultist":
            incantation = Monster_Action.id_map[self.name]["Incantation"]
            dark_strike = Monster_Action.id_map[self.name]["Dark Strike"]

            if game_state.turn == 1:
                intents.append(Monster_Action(incantation, 3, 1))
            else:
                intents.append(Monster_Action(dark_strike, 6, 1))

        elif self.monster_id == "FuzzyLouseNormal":
            # This needs to be gotten from the original json data and then saved over time
            d = random.randrange(5, 7)

            bite = Monster_Action.id_map[self.monster_id]["Bite"]
            grow = Monster_Action.id_map[self.monster_id]["Grow"]

            if self.last_move_id == self.second_last_move_id and self.second_last_move_id == bite:
                intents.append(Monster_Action(grow, 0, 1))

            elif self.last_move_id == self.second_last_move_id and self.second_last_move_id == grow:
                intents.append(Monster_Action(bite, d, 1))

            else:
                intents.append(Monster_Action(bite, d, 3/4))
                intents.append(Monster_Action(grow, 0, 1/4))

        elif self.monster_id == "FuzzyLouseDefensive":
            d = random.randrange(5, 7)

            bite = Monster_Action.id_map[self.monster_id]["Bite"]
            spit_web = Monster_Action.id_map[self.monster_id]["Spit Web"]

            if self.last_move_id == self.second_last_move_id and self.second_last_move_id == bite:
                intents.append(Monster_Action(spit_web, 0, 1))

            elif self.last_move_id == self.second_last_move_id and self.second_last_move_id == spit_web:
                intents.append(Monster_Action(bite, d, 1))

            else:
                intents.append(Monster_Action(bite, d, 3/4))
                intents.append(Monster_Action(spit_web, 0, 1/4))

        elif self.name == "Spike Slime (L)":
            flame_tackle = Monster_Action.id_map[self.name]["Flame Tackle"]
            lick = Monster_Action.id_map[self.name]["Lick"]
            if self.last_move_id == flame_tackle and self.second_last_move_id == flame_tackle:
                intents.append(Monster_Action(lick, 11, 1))

            elif self.last_move_id == lick and self.second_last_move_id == lick:
                intents.append(Monster_Action(flame_tackle, 7, 1))

            else:
                intents.append(Monster_Action(flame_tackle, 7, 7/10))
                intents.append(Monster_Action(lick, 11, 3/10))

        elif self.name == "Spike Slime (M)":
            flame_tackle = Monster_Action.id_map[self.name]["Flame Tackle"]
            lick = Monster_Action.id_map[self.name]["Lick"]
            if self.last_move_id == flame_tackle and self.second_last_move_id == flame_tackle:
                intents.append(Monster_Action(lick, 11, 1))

            elif self.last_move_id == lick and self.second_last_move_id == lick:
                intents.append(Monster_Action(flame_tackle, 7, 1))

            else:
                intents.append(Monster_Action(flame_tackle, 7, 7/10))
                intents.append(Monster_Action(lick, 11, 3/10))

        elif self.name == "Spike Slime (S)":
            tackle = Monster_Action.id_map[self.name]["Tackle"]
            intents.append(Monster_Action(tackle, 3, 1))

        elif self.name == "Acid Slime (M)":
            corrosive_spit = Monster_Action.id_map[self.name]["Corrosive Spit"]
            lick = Monster_Action.id_map[self.name]["Lick"]
            tackle = Monster_Action.id_map[self.name]["Tackle"]

            if self.last_move_id == tackle:
                intents.append(Monster_Action(lick, 11, 1/2))
                intents.append(Monster_Action(corrosive_spit, 7, 1/2))

            elif self.last_move_id == corrosive_spit and self.second_last_move_id == corrosive_spit:
                intents.append(Monster_Action(tackle, 11, 4/7))
                intents.append(Monster_Action(lick, 3, 3/7))

            elif self.last_move_id == lick and self.second_last_move_id == lick:
                intents.append(Monster_Action(corrosive_spit, 3, 3/7))
                intents.append(Monster_Action(tackle, 7, 4/7))

            else:
                intents.append(Monster_Action(tackle, 3, 4/10))
                intents.append(Monster_Action(corrosive_spit, 7, 3/10))
                intents.append(Monster_Action(lick, 11, 3/10))

        elif self.name == "Acid Slime (L)":
            corrosive_spit = Monster_Action.id_map[self.name]["Corrosive Spit"]
            lick = Monster_Action.id_map[self.name]["Lick"]
            tackle = Monster_Action.id_map[self.name]["Tackle"]

            if self.last_move_id == tackle:
                intents.append(Monster_Action(lick, 11, 1/2))
                intents.append(Monster_Action(corrosive_spit, 7, 1/2))

            elif self.last_move_id == corrosive_spit and self.second_last_move_id == corrosive_spit:
                intents.append(Monster_Action(tackle, 11, 4/7))
                intents.append(Monster_Action(lick, 3, 3/7))

            elif self.last_move_id == lick and self.second_last_move_id == lick:
                intents.append(Monster_Action(corrosive_spit, 3, 3/7))
                intents.append(Monster_Action(tackle, 7, 4/7))

            else:
                intents.append(Monster_Action(tackle, 3, 4/10))
                intents.append(Monster_Action(corrosive_spit, 7, 3/10))
                intents.append(Monster_Action(lick, 11, 3/10))

        elif self.name == "Acid Slime (S)":
            lick = Monster_Action.id_map[self.name]["Lick"]
            tackle = Monster_Action.id_map[self.name]["Tackle"]

            if self.last_move_id == lick:
                intents.append(Monster_Action(tackle, 3, 1))
            elif self.last_move_id == tackle:
                intents.append(Monster_Action(lick, 3, 1))

        elif self.name == "Gremlin Nob":
            bellow = Monster_Action.id_map[self.name]["Bellow"]
            bellow_damage = Move.monster_move_data[(self.name, bellow)][0]
            rush = Monster_Action.id_map[self.name]["Rush"]
            rush_damage = Move.monster_move_data[(self.name, bellow)][0]
            skull_bash = Monster_Action.id_map[self.name]["Skull Bash"]
            skull_bash_damage = Move.monster_move_data[(
                self.name, skull_bash)][0]

            if game_state.turn == 1:
                intents.append(Monster_Action(bellow, bellow_damage, 1))
            elif self.second_last_move_id == rush and self.last_move_id == rush:
                intents.append(Monster_Action(rush, rush_damage, 1))
            else:
                intents.append(Monster_Action(rush, rush_damage, 2/3))
                intents.append(Monster_Action(
                    skull_bash, skull_bash_damage, 1/3))

        elif self.name == "Sentry":
            beam = Monster_Action.id_map[self.name]["Beam"]
            beam_damage = Move.monster_move_data[(self.name, beam)][0]
            bolt = Monster_Action.id_map[self.name]["Bolt"]
            bolt_damage = Move.monster_move_data[(self.name, bolt)][0]

            if self.last_move_id == beam:
                intents.append(Monster_Action(bolt, bolt_damage, 1))
            elif self.last_move_id == bolt:
                intents.append(Monster_Action(beam, beam_damage, 1))
            else:
                sentry_num = game_state.monsters.index(self)

                if sentry_num == 0 or sentry_num == 2:
                    intents.append(Monster_Action(bolt, bolt_damage, 1))
                else:
                    intents.append(Monster_Action(beam, beam_damage, 1))

        elif self.name == "Lagavulin":
            attack = Monster_Action.id_map[self.name]["Attack"]
            attack_damage = Move.monster_move_data[(self.name, attack)][0]

            siphon_soul = Monster_Action.id_map[self.name]["Siphon Soul"]
            siphon_soul_damage = Move.monster_move_data[(
                self.name, siphon_soul)][0]

            sleep = Monster_Action.id_map[self.name]["Sleep"]
            sleep_damage = Move.monster_move_data[(self.name, sleep)][0]

            stun = Monster_Action.id_map[self.name]["Stun"]
            stun_damage = Move.monster_move_data[(self.name, stun)][0]

            if game_state.turn < 4 and self.current_hp == self.max_hp:
                intents.append(Monster_Action(sleep, sleep_damage, 1))

            elif self.second_last_move_id == attack and self.last_move_id == attack:
                intents.append(Monster_Action(
                    siphon_soul, siphon_soul_damage, 1))
            else:
                intents.append(Monster_Action(attack, attack_damage, 1))

        elif self.name == "Looter":
            mug = Monster_Action.id_map[self.name]["Mug"]
            mug_damage = Move.monster_move_data[(self.name, mug)][0]
            lunge = Monster_Action.id_map[self.name]["Lunge"]
            lunge_damage = Move.monster_move_data[(self.name, lunge)][0]
            smoke_bomb = Monster_Action.id_map[self.name]["Smoke Bomb"]
            smoke_bomb_damage = Move.monster_move_data[(
                self.name, smoke_bomb)][0]

            if game_state.turn == 1 or game_state.turn == 2:
                intents.append(Monster_Action(mug, mug_damage, 1))
            elif game_state.turn == 3:
                intents.append(Monster_Action(
                    smoke_bomb, smoke_bomb_damage, 1/2))
                intents.append(Monster_Action(lunge, lunge_damage, 1/2))
            else:
                intents.append(Monster_Action(
                    smoke_bomb, smoke_bomb_damage, 1))

        elif self.name == "Fungi Beast":
            bite = Monster_Action.id_map[self.name]["Bite"]
            bite_damage = Move.monster_move_data[(self.name, bite)][0]
            grow = Monster_Action.id_map[self.name]["Grow"]
            grow_damage = Move.monster_move_data[(self.name, grow)][0]

            if self.second_last_move_id == bite and self.last_move_id == bite:
                intents.append(Monster_Action(grow, grow_damage, 1))
            elif self.last_move_id == grow:
                intents.append(Monster_Action(bite, bite_damage, 1))
            else:
                intents.append(Monster_Action(bite, bite_damage, 3/5))
                intents.append(Monster_Action(grow, grow_damage, 2/5))

        elif self.name == "Hexaghost":
            order = (game_state.turn-3) % 7

            activate = Monster_Action.id_map[self.name]["Activate"]
            divider = Monster_Action.id_map[self.name]["Divider"]
            # Move.monster_move_data[(self.name, divider)][0]
            divider_damage = game_state.current_hp / 12 + 1

            sear = Monster_Action.id_map[self.name]["Sear"]
            sear_damage = Move.monster_move_data[(self.name, sear)][0]
            tackle = Monster_Action.id_map[self.name]["Tackle"]
            tackle_damage = Move.monster_move_data[(self.name, tackle)][0]
            inflame = Monster_Action.id_map[self.name]["Inflame"]
            inflame_damage = Move.monster_move_data[(self.name, inflame)][0]
            inferno = Monster_Action.id_map[self.name]["Inferno"]
            inferno_damage = Move.monster_move_data[(self.name, inflame)][0]

            if game_state.turn == 1:
                intents.append(Monster_Action(activate, 0, 1))
            elif game_state.turn == 2:
                intents.append(Monster_Action(divider, divider_damage, 1))
            elif order == 0 or order == 2 or order == 5:
                intents.append(Monster_Action(sear, sear_damage, 1))
            elif order == 1 or order == 4:
                intents.append(Monster_Action(tackle, tackle_damage, 1))
            elif order == 4:
                intents.append(Monster_Action(inflame, inflame_damage, 1))
            elif order == 6:
                intents.append(Monster_Action(inferno, inferno_damage, 1))

        elif self.name == "Slime Boss":
            order = (game_state.turn - 1) % 3

            goop_spray = Monster_Action.id_map[self.name]["Goop Spray"]
            goop_spray_damage = Move.monster_move_data[(
                self.name, goop_spray)][0]
            preparing = Monster_Action.id_map[self.name]["Preparing"]
            slam = Monster_Action.id_map[self.name]["Slam"]
            slam_damage = Move.monster_move_data[(self.name, slam)][0]

            if order == 0:
                intents.append(Monster_Action(
                    goop_spray, goop_spray_damage, 1))
            elif order == 1:
                intents.append(Monster_Action(preparing, 0, 1))
            elif order == 2:
                intents.append(Monster_Action(slam, slam_damage, 1))

        elif self.name == "Blue Slaver":
            stab = Monster_Action.id_map[self.name]["Stab"]
            stab_damage = Move.monster_move_data[(self.name, stab)][0]

            rake = Monster_Action.id_map[self.name]["Rake"]
            rake_damage = Move.monster_move_data[(self.name, rake)][0]

            if self.last_move_id == stab and self.second_last_move_id == stab:
                intents.append(Monster_Action(rake, rake_damage, 1))

            if self.last_move_id == rake and self.second_last_move_id == rake:
                intents.append(Monster_Action(stab, stab_damage, 1))

            else:
                intents.append(Monster_Action(rake, rake_damage, 2/5))
                intents.append(Monster_Action(stab, stab_damage, 3/5))

        elif self.name == "Red Slaver":
            has_been_entangeled = False

            stab = Monster_Action.id_map[self.name]["Stab"]
            stab_damage = Move.monster_move_data[(self.name, stab)][0]

            scrape = Monster_Action.id_map[self.name]["Scrape"]
            scrape_damage = Move.monster_move_data[(self.name, rake)][0]

            entangle = Monster_Action.id_map[self.name]["Entangle"]
            entangle_damage = Move.monster_move_data[(self.name, rake)][0]

            # if has_been_entangeled:

            # else:

        elif self.name == "Fat Gremlin":
            smash = Monster_Action.id_map[self.name]["Smash"]
            smash_damage = Move.monster_move_data[(self.name, smash)][0]

            intents.append(Monster_Action(smash, smash_damage, 1))

        elif self.name == "Mad Gremlin":
            scratch = Monster_Action.id_map[self.name]["Scratch"]
            scratch_damage = Move.monster_move_data[(self.name, scratch)][0]

            intents.append(Monster_Action(scratch, scratch_damage, 1))

        elif self.name == "Shield Gremlin":
            protect = Monster_Action.id_map[self.name]["Protect"]
            protect_damage = Move.monster_move_data[(self.name, protect)][0]

            shield_bash = Monster_Action.id_map[self.name]["Shield Bash"]
            shield_bash_damage = Move.monster_move_data[(
                self.name, shield_bash)][0]

            if len(game_state.monsters) > 1:
                intents.append(Monster_Action(protect, protect_damage, 1))

            else:
                intents.append(Monster_Action(
                    shield_bash, shield_bash_damage, 1))

        elif self.name == "Sneaky Gremlin":
            puncture = Monster_Action.id_map[self.name]["Puncture"]
            puncture_damage = Move.monster_move_data[(self.name, puncture)][0]

            intents.append(Monster_Action(puncture, puncture_damage, 1))

        elif self.name == "Gremlin Wizard":
            charging = Monster_Action.id_map[self.name]["Charging"]
            charging_damage = Move.monster_move_data[(self.name, charging)][0]

            ultimate_blast = Monster_Action.id_map[self.name]["Ultimate Blast"]
            ultimate_blast_damage = Move.monster_move_data[(
                self.name, ultimate_blast)][0]

            if game_state.turn % 4 == 3:
                intents.append(Monster_Action(
                    ultimate_blast, ultimate_blast_damage, 1))
            else:
                intents.append(Monster_Action(charging, charging_damage, 1))

        elif self.name == "The Guardian":
            charging_up = Monster_Action.id_map[self.name]["Charging Up"]
            charging_up_damage = Move.monster_move_data[(
                self.name, charging_up)][0]

            fierce_bash = Monster_Action.id_map[self.name]["Fierce Bash"]
            fierce_bash_damage = Move.monster_move_data[(
                self.name, fierce_bash)][0]

            vent_steam = Monster_Action.id_map[self.name]["Vent Steam"]
            vent_steam_damage = Move.monster_move_data[(
                self.name, vent_steam)][0]

            whirlwind = Monster_Action.id_map[self.name]["Whirlwind"]
            whirlwind_damage = Move.monster_move_data[(
                self.name, whirlwind)][0]

            defensive_mode = Monster_Action.id_map[self.name]["Defensive Mode"]
            defensive_mode_damage = Move.monster_move_data[(
                self.name, defensive_mode)][0]

            roll_attack = Monster_Action.id_map[self.name]["Roll Attack"]
            roll_attack_damage = Move.monster_move_data[(
                self.name, roll_attack)][0]

            twin_slam = Monster_Action.id_map[self.name]["Twin Slam"]
            twin_slam_damage = Move.monster_move_data[(
                self.name, twin_slam)][0]

            mode_shift = 1
            sharp_hide = 3
            try:
                index = [i.power_name for i in self.powers].index("Mode Shift")
                mode_shift = self.powers[index]
            except ValueError:
                mode_shift = 0
            try:
                index = [i.power_name for i in self.powers].index("Sharp Hide")
                sharp_hide = self.powers[index]
            except ValueError:
                sharp_hide = 0

            if (mode_shift <= 0 and sharp_hide == 0):
                intents.append(Monster_Action(
                    defensive_mode, defensive_mode_damage, 1))

            elif game_state.turn == 1 or self.last_move_id == whirlwind \
                    or self.last_move_id == twin_slam:
                intents.append(Monster_Action(
                    charging_up, charging_up_damage, 1))
            elif self.last_move_id == charging_up:
                intents.append(Monster_Action(
                    fierce_bash, fierce_bash_damage, 1))
            elif self.last_move_id == fierce_bash:
                intents.append(Monster_Action(
                    vent_steam, vent_steam_damage, 1))
            elif self.last_move_id == vent_steam:
                intents.append(Monster_Action(whirlwind, whirlwind_damage, 1))

            elif self.last_move_id == defensive_mode:
                intents.append(Monster_Action(
                    roll_attack, roll_attack_damage, 1))
            elif self.last_move_id == roll_attack:
                intents.append(Monster_Action(twin_slam, twin_slam_damage, 1))

        return intents

    def __eq__(self, other):
        if (other == None):
            return False
        if self.name == other.name and self.current_hp == other.current_hp and self.max_hp == other.max_hp and self.block == other.block:
            if len(self.powers) == len(other.powers):
                for i in range(len(self.powers)):
                    if self.powers[i] != other.powers[i]:
                        return False
                return True
        return False


class Move:

    # data format: (monster name, moveid) : (damage, block, # hits, self powers, target powers, cards added to deck), exhaust, draw cards, aoe
    monster_move_data = {
        ("Jaw Worm", Monster_Action.id_map["Jaw Worm"]["Chomp"]): (11, 0, 1, [], [], [], False, 0, False),
        ("Jaw Worm", Monster_Action.id_map["Jaw Worm"]["Bellow"]): (0, 6, 0, [("Strength", 3)], [], [], False, 0, False),
        ("Jaw Worm", Monster_Action.id_map["Jaw Worm"]["Thrash"]): (7, 5, 1, [], [], [], False, 0, False),

        ("FuzzyLouseNormal", Monster_Action.id_map["FuzzyLouseNormal"]["Bite"]): (7, 0, 1, [], [], [], False, 0, False),
        ("FuzzyLouseNormal", Monster_Action.id_map["FuzzyLouseNormal"]["Grow"]): (0, 0, 0, [("Strength", 3)], [], [], False, 0, False),

        ("FuzzyLouseDefensive", Monster_Action.id_map["FuzzyLouseDefensive"]["Bite"]): (7, 0, 1, [], [], [], False, 0, False),
        ("FuzzyLouseDefensive", Monster_Action.id_map["FuzzyLouseDefensive"]["Spit Web"]): (0, 0, 0, [], [("Weak", 2)], [], False, 0, False),

        ("Cultist", Monster_Action.id_map["Cultist"]["Incantation"]): (0, 0, 0, [("Ritual", 3)], [], [], False, 0, False),
        ("Cultist", Monster_Action.id_map["Cultist"]["Dark Strike"]): (6, 0, 1, [], [], [], False, 0, False),

        ("Acid Slime (L)", Monster_Action.id_map["Acid Slime (L)"]["Corrosive Spit"]): (11, 0, 1, [], [], [("Slimed", 2), ("Slimed", 2)], False, 0, False),
        ("Acid Slime (L)", Monster_Action.id_map["Acid Slime (L)"]["Lick"]): (0, 0, 0, [], [("Weak", 2)], [], False, 0, False),
        ("Acid Slime (L)", Monster_Action.id_map["Acid Slime (L)"]["Tackle"]): (16, 0, 1, [], [], [], False, 0, False),
        ("Acid Slime (L)", Monster_Action.id_map["Acid Slime (L)"]["Split"]): (0, 0, 0, [], [], [], False, 0, False),

        ("Spike Slime (L)", Monster_Action.id_map["Spike Slime (L)"]["Flame Tackle"]): (16, 0, 1, [], [], [("Slimed", 2), ("Slimed", 2)], False, 0, False),
        ("Spike Slime (L)", Monster_Action.id_map["Spike Slime (L)"]["Lick"]): (0, 0, 0, [], [("Frail", 2)], [], False, 0, False),
        ("Spike Slime (L)", Monster_Action.id_map["Spike Slime (L)"]["Split"]): (0, 0, 0, [], [], [], False, 0, False),


        ("Acid Slime (M)", Monster_Action.id_map["Acid Slime (M)"]["Corrosive Spit"]): (7, 0, 1, [], [], [("Slimed", 2)], False, 0, False),
        ("Acid Slime (M)", Monster_Action.id_map["Acid Slime (M)"]["Lick"]): (0, 0, 0, [], [("Weak", 1)], [], False, 0, False),
        ("Acid Slime (M)", Monster_Action.id_map["Acid Slime (M)"]["Tackle"]): (10, 0, 1, [], [], [], False, 0, False),

        ("Spike Slime (M)", Monster_Action.id_map["Spike Slime (M)"]["Flame Tackle"]): (8, 0, 1, [], [], [("Slimed", 2)], False, 0, False),
        ("Spike Slime (M)", Monster_Action.id_map["Spike Slime (M)"]["Lick"]): (0, 0, 0, [], [("Frail", 1)], [], False, 0, False),

        ("Acid Slime (S)", Monster_Action.id_map["Acid Slime (S)"]["Lick"]): (0, 0, 0, [], [("Weak", 1)], [], False, 0, False),
        ("Acid Slime (S)", Monster_Action.id_map["Acid Slime (S)"]["Tackle"]): (3, 0, 1, [], [], [], False, 0, False),

        ("Spike Slime (S)", Monster_Action.id_map["Spike Slime (S)"]["Tackle"]): (5, 0, 1, [], [], [], False, 0, False),

        ("Looter", Monster_Action.id_map["Looter"]["Mug"]): (10, 0, 1, [], [], [], False, 0, False),
        ("Looter", Monster_Action.id_map["Looter"]["Lunge"]): (12, 0, 1, [], [], [], False, 0, False),
        ("Looter", Monster_Action.id_map["Looter"]["Smoke Bomb"]): (0, 6, 0, [], [], [], False, 0, False),
        ("Looter", Monster_Action.id_map["Looter"]["Escape"]): (0, 0, 0, [], [], [], False, 0, False),

        ("Fungi Beast", Monster_Action.id_map["Fungi Beast"]["Bite"]): (6, 0, 1, [], [], [], False, 0, False),
        ("Fungi Beast", Monster_Action.id_map["Fungi Beast"]["Grow"]): (0, 0, 0, [("Strength", 3)], [], [], False, 0, False),

        ("Hexaghost", Monster_Action.id_map["Hexaghost"]["Activate"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Hexaghost", Monster_Action.id_map["Hexaghost"]["Divider"]): (0, 0, 6, [], [], [], False, 0, False),
        ("Hexaghost", Monster_Action.id_map["Hexaghost"]["Inferno"]): (2, 0, 6, [], [], [("Burn", 3)], False, 0, False),
        ("Hexaghost", Monster_Action.id_map["Hexaghost"]["Sear"]): (6, 0, 1, [], [], [("Burn", 1)], False, 0, False),
        ("Hexaghost", Monster_Action.id_map["Hexaghost"]["Tackle"]): (5, 0, 2, [], [], [], False, 0, False),
        ("Hexaghost", Monster_Action.id_map["Hexaghost"]["Inflame"]): (0, 12, 0, [("Strength", 2)], [], [], False, 0, False),

        ("Slime Boss", Monster_Action.id_map["Slime Boss"]["Goop Spray"]): (0, 0, 0, [], [], [("Slimed", 3)], False, 0, False),
        ("Slime Boss", Monster_Action.id_map["Slime Boss"]["Preparing"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Slime Boss", Monster_Action.id_map["Slime Boss"]["Slam"]): (35, 0, 1, [], [], [], False, 0, False),
        ("Slime Boss", Monster_Action.id_map["Slime Boss"]["Split"]): (0, 0, 0, [], [], [], False, 0, False),

        ("The Guardian", Monster_Action.id_map["The Guardian"]["Charging Up"]): (0, 9, 0, [], [], [], False, 0, False),
        ("The Guardian", Monster_Action.id_map["The Guardian"]["Fierce Bash"]): (32, 0, 1, [], [], [], False, 0, False),
        ("The Guardian", Monster_Action.id_map["The Guardian"]["Vent Steam"]): (0, 0, 0, [], [("Vulnerable", 2), ("Weak", 2)], [], False, 0, False),
        ("The Guardian", Monster_Action.id_map["The Guardian"]["Whirlwind"]): (5, 0, 4, [], [], [], False, 0, False),

        ("The Guardian", Monster_Action.id_map["The Guardian"]["Defensive Mode"]): (0, 0, 0, [("Sharp Hide", 3)], [], [], False, 0, False),
        ("The Guardian", Monster_Action.id_map["The Guardian"]["Roll Attack"]): (9, 0, 1, [], [], [], False, 0, False),
        # NOTE: Mode shift goes up by 10 each time, but this is an estimation, right.....?
        ("The Guardian", Monster_Action.id_map["The Guardian"]["Twin Slam"]): (8, 0, 2, [("Sharp Hide", -3), ("Mode Shift", 40)], [], [], False, 0, False),

        ("Gremlin Nob", Monster_Action.id_map["Gremlin Nob"]["Bellow"]): (0, 0, 0, [("Enrage", 2)], [], [], False, 0, False),
        ("Gremlin Nob", Monster_Action.id_map["Gremlin Nob"]["Rush"]): (14, 0, 1, [], [], [], False, 0, False),
        ("Gremlin Nob", Monster_Action.id_map["Gremlin Nob"]["Skull Bash"]): (6, 0, 1, [], [("Vulnerable", 2)], [], False, 0, False),

        ("Sentry", Monster_Action.id_map["Sentry"]["Beam"]): (9, 0, 1, [], [], [], False, 0, False),
        ("Sentry", Monster_Action.id_map["Sentry"]["Bolt"]): (0, 0, 0, [], [], [("Dazed", 2)], False, 0, False),

        ("Lagavulin", Monster_Action.id_map["Lagavulin"]["Attack"]): (18, 0, 1, [], [], [], False, 0, False),
        ("Lagavulin", Monster_Action.id_map["Lagavulin"]["Siphon Soul"]): (0, 0, 0, [], [("Dexterity", -1), ("Strength", -1)], [], False, 0, False),
        ("Lagavulin", Monster_Action.id_map["Lagavulin"]["Sleep"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Lagavulin", Monster_Action.id_map["Lagavulin"]["Stun"]): (0, 0, 0, [], [], [], False, 0, False),

        ("Fat Gremlin", Monster_Action.id_map["Fat Gremlin"]["Smash"]): (4, 0, 1, [("Weakness", 1)], [], [], False, 0, False),

        ("Mad Gremlin", Monster_Action.id_map["Mad Gremlin"]["Scratch"]): (4, 0, 1, [], [], [], False, 0, False),

        ("Shield Gremlin", Monster_Action.id_map["Shield Gremlin"]["Protect"]): (0, 7, 0, [], [], [], False, 0, False),
        ("Shield Gremlin", Monster_Action.id_map["Shield Gremlin"]["Shield Bash"]): (6, 0, 1, [], [], [], False, 0, False),

        ("Sneaky Gremlin", Monster_Action.id_map["Sneaky Gremlin"]["Puncture"]): (9, 0, 1, [], [], [], False, 0, False),

        ("Gremlin Wizard", Monster_Action.id_map["Gremlin Wizard"]["Charging"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Gremlin Wizard", Monster_Action.id_map["Gremlin Wizard"]["Ultimate Blast"]): (25, 0, 1, [], [], [], False, 0, False),

        ("SlaverBlue", Monster_Action.id_map["SlaverBlue"]["Stab"]): (12, 0, 1, [], [], [], False, 0, False),
        ("SlaverBlue", Monster_Action.id_map["SlaverBlue"]["Rake"]): (7, 0, 1, [], [("Weakness", 1)], [], False, 0, False),

        ("SlaverRed", Monster_Action.id_map["SlaverRed"]["Stab"]): (13, 0, 1, [], [], [], False, 0, False),
        ("SlaverRed", Monster_Action.id_map["SlaverRed"]["Scrape"]): (8, 0, 1, [], [("Vulnerable", 1)], [], False, 0, False),
        ("SlaverRed", Monster_Action.id_map["SlaverRed"]["Entangle"]): (0, 0, 0, [], [("Entangled", 1)], [], False, 0, False),

        ("Shelled Parasite", Monster_Action.id_map["Shelled Parasite"]["Double Strike"]): (8, 0, 2, [], [], [], False, 0, False),
        ("Shelled Parasite", Monster_Action.id_map["Shelled Parasite"]["Suck"]): (10, 0, 1, [], [], [], False, 0, False),
        ("Shelled Parasite", Monster_Action.id_map["Shelled Parasite"]["Fell"]): (16, 0, 1, [], [("Frail", 2)], [], False, 0, False),

        ("Spheric Guardian", Monster_Action.id_map["Spheric Guardian"]["Slam"]): (10, 0, 2, [], [], [], False, 0, False),
        ("Spheric Guardian", Monster_Action.id_map["Spheric Guardian"]["Activate"]): (0, 25, 0, [], [], [], False, 0, False),
        ("Spheric Guardian", Monster_Action.id_map["Spheric Guardian"]["Harden"]): (10, 15, 1, [], [], [], False, 0, False),
        ("Spheric Guardian", Monster_Action.id_map["Spheric Guardian"]["Attack/Debuff"]): (10, 0, 0, [], [("Frail", 5)], [], False, 0, False),


        ("Centurion", Monster_Action.id_map["Centurion"]["Slash"]): (12, 0, 1, [], [], [], False, 0, False),
        ("Centurion", Monster_Action.id_map["Centurion"]["Fury"]): (6, 0, 3, [], [], [], False, 0, False),
        ("Centurion", Monster_Action.id_map["Centurion"]["Defend"]): (0, 0, 0, [], [], [], False, 0, False),

        ("Mystic", Monster_Action.id_map["Mystic"]["Heal"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Mystic", Monster_Action.id_map["Mystic"]["Buff"]): (0, 0, 0, [("Strength", 2)], [], [], False, 0, False),
        ("Mystic", Monster_Action.id_map["Mystic"]["Attack/Debuff"]): (8, 0, 1, [], [("Frail", 2)], [], False, 0, False),

        ("Snake Plant", Monster_Action.id_map["Snake Plant"]["Chomp"]): (7, 0, 3, [], [], [], False, 0, False),
        ("Snake Plant", Monster_Action.id_map["Snake Plant"]["Enfeebling Spores"]): (0, 0, 0, [], [("Frail", 2), ("Weak", 2)], [], False, 0, False),

        ("Snecko", Monster_Action.id_map["Snecko"]["Perplexing Glare"]): (0, 0, 0, [], [("Confused", 1)], [], False, 0, False),
        ("Snecko", Monster_Action.id_map["Snecko"]["Tail Whip"]): (8, 0, 1, [], [("Vulnerable", 2)], [], False, 0, False),
        ("Snecko", Monster_Action.id_map["Snecko"]["Bite"]): (15, 0, 1, [], [], [], False, 0, False),

        ("Byrd", Monster_Action.id_map["Byrd"]["Caw"]): (0, 0, 0, [("Strength", 1)], [], [], False, 0, False),
        ("Byrd", Monster_Action.id_map["Byrd"]["Peck"]): (1, 0, 5, [], [], [], False, 0, False),
        ("Byrd", Monster_Action.id_map["Byrd"]["Swoop"]): (12, 0, 1, [], [], [], False, 0, False),
        ("Byrd", Monster_Action.id_map["Byrd"]["Fly"]): (0, 0, 0, [("Flying", 3)], [], [], False, 0, False),
        ("Byrd", Monster_Action.id_map["Byrd"]["Headbutt"]): (3, 0, 1, [], [], [], False, 0, False),
        ("Byrd", Monster_Action.id_map["Byrd"]["Stun"]): (0, 0, 0, [], [], [], False, 0, False),

        # TODO: Implement confused
        ("Chosen", Monster_Action.id_map["Chosen"]["Poke"]): (5, 0, 2, [], [], [], False, 0, False),
        ("Chosen", Monster_Action.id_map["Chosen"]["Zap"]): (18, 0, 1, [], [], [], False, 0, False),
        ("Chosen", Monster_Action.id_map["Chosen"]["Debilitate"]): (10, 0, 1, [], [("Vulnerable", 2)], [], False, 0, False),
        ("Chosen", Monster_Action.id_map["Chosen"]["Drain"]): (0, 0, 0, [("Strength", 3)], [("Weak", 3)], [], False, 0, False),
        ("Chosen", Monster_Action.id_map["Chosen"]["Hex"]): (0, 0, 0, [], [("Hex", 1)], [], False, 0, False),

        ("Mugger", Monster_Action.id_map["Mugger"]["Mug"]): (10, 0, 1, [], [], [], False, 0, False),
        ("Mugger", Monster_Action.id_map["Mugger"]["Lunge"]): (16, 0, 1, [], [], [], False, 0, False),
        ("Mugger", Monster_Action.id_map["Mugger"]["Smoke Bomb"]): (0, 11, 0, [], [], [], False, 0, False),
        ("Mugger", Monster_Action.id_map["Mugger"]["Escape"]): (0, 0, 0, [], [], [], False, 0, False),

        ("Pointy",  Monster_Action.id_map["Pointy"]["Attack"]): (5, 0, 2, [], [], [], False, 0, False),

        ("Romeo",  Monster_Action.id_map["Romeo"]["Mock"]): (6, 0, 2, [], [], [], False, 0, False),
        ("Romeo",  Monster_Action.id_map["Romeo"]["Agonizing Slash"]): (10, 0, 1, [], [("Weakness", 2)], [], False, 0, False),
        ("Romeo",  Monster_Action.id_map["Romeo"]["Cross Slash"]): (15, 0, 1, [], [], [], False, 0, False),

        ("Bear",  Monster_Action.id_map["Bear"]["Bear Hug"]): (0, 0, 0, [], [("Dexterity", -2)], [], False, 0, False),
        ("Bear",  Monster_Action.id_map["Bear"]["Lunge"]): (9, 9, 1, [], [], [], False, 0, False),
        ("Bear",  Monster_Action.id_map["Bear"]["Maul"]): (18, 0, 1, [], [], [], False, 0, False),

        # TODO: Deal with the variability about number of multi-stab hits
        ("Book of Stabbing", Monster_Action.id_map["Book of Stabbing"]["Multi-Stab"]): (6, 0, 1, [], [], [], False, 0, False),
        ("Book of Stabbing", Monster_Action.id_map["Book of Stabbing"]["Single Stab"]): (21, 0, 1, [], [], [], False, 0, False),

        # TODO: add summoning of minions
        ("Gremlin Leader", Monster_Action.id_map["Gremlin Leader"]["Encourage"]): (0, 0, 0, [("Strength", 3)], [], [], False, 0, False),
        ("Gremlin Leader", Monster_Action.id_map["Gremlin Leader"]["Rally!"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Gremlin Leader", Monster_Action.id_map["Gremlin Leader"]["Stab"]): (6, 0, 3, [], [], [], False, 0, False),

        ("Taskmaster", Monster_Action.id_map["Taskmaster"]["Scouring Whip"]): (7, 0, 1, [], [], [("Wound", 1)], False, 0, False),

        ("Bronze Automaton", Monster_Action.id_map["Bronze Automaton"]["Spawn Orbs"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Bronze Automaton", Monster_Action.id_map["Bronze Automaton"]["Boost"]): (0, 9, 0, [("Strength", 3)], [], [], False, 0, False),
        ("Bronze Automaton", Monster_Action.id_map["Bronze Automaton"]["Flail"]): (7, 0, 2, [], [], [], False, 0, False),
        ("Bronze Automaton", Monster_Action.id_map["Bronze Automaton"]["HYPER BEAM"]): (45, 0, 1, [], [], [], False, 0, False),
        ("Bronze Automaton", Monster_Action.id_map["Bronze Automaton"]["Stun"]): (0, 0, 0, [], [], [], False, 0, False),

        ("Orb", Monster_Action.id_map["Orb"]["Stasis"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Orb", Monster_Action.id_map["Orb"]["Beam"]): (8, 0, 1, [], [], [], False, 0, False),
        ("Orb", Monster_Action.id_map["Orb"]["Support Beam"]): (0, 0, 0, [], [], [], False, 0, False),


        ("The Champ", Monster_Action.id_map["The Champ"]["Execute"]): (10, 0, 2, [], [], [], False, 0, False),
        ("The Champ", Monster_Action.id_map["The Champ"]["Heavy Slash"]): (16, 0, 1, [], [], [], False, 0, False),
        ("The Champ", Monster_Action.id_map["The Champ"]["Defensive Stance"]): (0, 15, 0, [("Metallicize", 5)], [], [], False, 0, False),
        ("The Champ", Monster_Action.id_map["The Champ"]["Face Slap"]): (12, 0, 1, [], [("Frail", 2), ("Vulnerable", 2)], [], False, 0, False),
        ("The Champ", Monster_Action.id_map["The Champ"]["Taunt"]): (0, 0, 0, [], [("Weak", 2), ("Vulnerable", 2)], [], False, 0, False),
        ("The Champ", Monster_Action.id_map["The Champ"]["Gloat"]): (0, 0, 0, [("Strength", 2)], [], [], False, 0, False),
        # TODO: remove all debuffs
        ("The Champ", Monster_Action.id_map["The Champ"]["Anger"]): (0, 0, 0, [("Strength", 6)], [], [], False, 0, False),

        ("The Collector", Monster_Action.id_map["The Collector"]["Buff"]): (0, 15, 0, [], [], [], False, 0, False),
        ("The Collector", Monster_Action.id_map["The Collector"]["Fireball"]): (18, 0, 1, [], [], [], False, 0, False),
        ("The Collector", Monster_Action.id_map["The Collector"]["Mega Debuff"]): (0, 0, 0, [], [("Weak", 3), ("Vulnerable", 3), ("Frail", 3)], [], False, 0, False),
        ("The Collector", 1): (0, 0, 0, [], [], [], False, 0, False),
        ("The Collector", 5): (0, 0, 0, [], [], [], False, 0, False),

        ("Torch Head", Monster_Action.id_map["Torch Head"]["Tackle"]): (7, 0, 1, [], [], [], False, 0, False),

        # TODO: Darkling Reincarnate
        ("Darkling", Monster_Action.id_map["Darkling"]["Nip"]): (11, 0, 1, [], [], [], False, 0, False),
        ("Darkling", Monster_Action.id_map["Darkling"]["Chomp"]): (8, 0, 2, [], [], [], False, 0, False),
        ("Darkling", Monster_Action.id_map["Darkling"]["Harden"]): (0, 12, 0, [], [], [], False, 0, False),
        ("Darkling", Monster_Action.id_map["Darkling"]["Reincarnate"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Darkling", Monster_Action.id_map["Darkling"]["Regrow"]): (0, 0, 0, [], [], [], False, 0, False),

        ("Orb Walker", Monster_Action.id_map["Orb Walker"]["Laser"]): (10, 0, 1, [], [], [("Burn", 0), ("Burn", 2)], False, 0, False),
        ("Orb Walker", Monster_Action.id_map["Orb Walker"]["Claw"]): (15, 0, 1, [], [], [], False, 0, False),

        ("Spiker", Monster_Action.id_map["Spiker"]["Cut"]): (7, 0, 1, [], [], [], False, 0, False),
        ("Spiker", Monster_Action.id_map["Spiker"]["Spike"]): (0, 0, 0, [("Thorns", 2)], [], [], False, 0, False),

        ("Exploder", Monster_Action.id_map["Exploder"]["Slam"]): (9, 0, 1, [], [], [], False, 0, False),
        ("Exploder", Monster_Action.id_map["Exploder"]["Explode"]): (30, 0, 1, [], [], [], False, 0, False),

        ("Repulsor", Monster_Action.id_map["Repulsor"]["Bash"]): (11, 0, 1, [], [], [], False, 0, False),
        ("Repulsor", Monster_Action.id_map["Repulsor"]["Repulse"]): (0, 0, 0, [], [], [("Dazed", 0), ("Dazed", 0)], False, 0, False),

        ("The Maw", Monster_Action.id_map["The Maw"]["Roar"]): (0, 0, 0, [], [("Weakness", 3), ("Frail", 3)], [], False, 0, False),
        ("The Maw", Monster_Action.id_map["The Maw"]["Drool"]): (0, 0, 0, [("Strength", 3)], [], [], False, 0, False),
        ("The Maw", Monster_Action.id_map["The Maw"]["Slam"]): (25, 0, 1, [], [], [], False, 0, False),
        ("The Maw", Monster_Action.id_map["The Maw"]["Nom"]): (5, 0, 1, [], [], [], False, 0, False),

        ("Spire Growth", Monster_Action.id_map["Spire Growth"]["Quick Tackle"]): (16, 0, 1, [], [], [], False, 0, False),
        ("Spire Growth", Monster_Action.id_map["Spire Growth"]["Smash"]): (22, 0, 1, [], [], [], False, 0, False),
        ("Spire Growth", Monster_Action.id_map["Spire Growth"]["Constrict"]): (0, 0, 0, [], [("Constricted", 10)], [], False, 0, False),

        ("Transient", Monster_Action.id_map["Transient"]["Attack"]): (30, 0, 1, [], [], [], False, 0, False),

        # TODO: Implant adding a card to the deck (Not Nessecary)
        ("Writhing Mass", Monster_Action.id_map["Writhing Mass"]["Implant"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Writhing Mass", Monster_Action.id_map["Writhing Mass"]["Flail"]): (15, 16, 1, [], [], [], False, 0, False),
        ("Writhing Mass", Monster_Action.id_map["Writhing Mass"]["Wither"]): (10, 0, 1, [], [("Weakness", 2), ("Vulnerable", 2)], [], False, 0, False),
        ("Writhing Mass", Monster_Action.id_map["Writhing Mass"]["Multi-Strike"]): (7, 0, 3, [], [], [], False, 0, False),
        ("Writhing Mass", Monster_Action.id_map["Writhing Mass"]["Strong Strike"]): (32, 0, 1, [], [], [], False, 0, False),

        # TODO: Giant Head does 5 more damage each time It Is time is used.
        ("Giant Head", Monster_Action.id_map["Giant Head"]["Count"]): (13, 0, 1, [], [], [], False, 0, False),
        ("Giant Head", Monster_Action.id_map["Giant Head"]["Glare"]): (0, 0, 0, [], [("Weakness", 1)], [], False, 0, False),
        ("Giant Head", Monster_Action.id_map["Giant Head"]["It Is Time"]): (30, 0, 1, [], [], [], False, 0, False),

        ("Nemesis", Monster_Action.id_map["Nemesis"]["Debuff"]): (0, 0, 0, [], [], [("Burn", 2), ("Burn", 2), ("Burn", 2)], False, 0, False),
        ("Nemesis", Monster_Action.id_map["Nemesis"]["Attack"]): (6, 0, 3, [], [], [], False, 0, False),
        ("Nemesis", Monster_Action.id_map["Nemesis"]["Scythe"]): (45, 0, 1, [], [], [], False, 0, False),

        ("Reptomancer", Monster_Action.id_map["Reptomancer"]["Summon"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Reptomancer", Monster_Action.id_map["Reptomancer"]["Snake Strike"]): (13, 0, 2, [], [("Weakness", 1)], [], False, 0, False),
        ("Reptomancer", Monster_Action.id_map["Reptomancer"]["Big Bite"]): (30, 0, 1, [], [], [], False, 0, False),

        ("Dagger", Monster_Action.id_map["Dagger"]["Stab"]): (9, 0, 1, [], [], [("Wound", 2)], False, 0, False),
        ("Dagger", Monster_Action.id_map["Dagger"]["Explode"]): (25, 0, 1, [], [], [], False, 0, False),


        # TODO: Rebirth removes all debuffs, and activates when Awakened One is at 0 (Maybe could be done by summoning a monster with 99999 hp that kills itself and summons phase 2 of awakened one)
        ("Awakened One", Monster_Action.id_map["Awakened One"]["Slash"]): (20, 0, 1, [], [], [], False, 0, False),
        ("Awakened One", Monster_Action.id_map["Awakened One"]["Soul Strike"]): (6, 0, 4, [], [], [], False, 0, False),
        ("Awakened One", Monster_Action.id_map["Awakened One"]["Rebirth"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Awakened One", Monster_Action.id_map["Awakened One"]["Dark Echo"]): (40, 0, 1, [], [], [], False, 0, False),
        ("Awakened One", Monster_Action.id_map["Awakened One"]["Sludge"]): (18, 0, 1, [], [], [("Void", 0)], False, 0, False),
        ("Awakened One", Monster_Action.id_map["Awakened One"]["Tackle"]): (10, 0, 3, [], [], [], False, 0, False),

        ("Donu", Monster_Action.id_map["Donu"]["Circle of Power"]): (0, 0, 0, [("Strength", 3)], [], [], False, 0, False),
        ("Donu", Monster_Action.id_map["Donu"]["Beam"]): (10, 0, 2, [], [], [], False, 0, False),

        ("Deca", Monster_Action.id_map["Deca"]["Square of Protection"]): (0, 0, 0, [], [], [], False, 0, False),
        ("Deca", Monster_Action.id_map["Deca"]["Beam"]): (10, 0, 2, [], [], [("Dazed", 2), ("Dazed", 2)], False, 0, False),

        # TODO: Time Eater Haste Heals back to 50% HP and loses all debuffs
        ("Time Eater", Monster_Action.id_map["Time Eater"]["Reverberate"]): (7, 0, 3, [], [], [], False, 0, False),
        ("Time Eater", Monster_Action.id_map["Time Eater"]["Head Slam"]): (26, 0, 1, [], [("Draw Reduction", 2)], [], False, 0, False),
        ("Time Eater", Monster_Action.id_map["Time Eater"]["Ripple"]): (0, 20, 0, [], [], [], False, 0, False),
        ("Time Eater", Monster_Action.id_map["Time Eater"]["Haste"]): (0, 0, 0, [], [], [], False, 0, False),

        # Playable Status Cards
        ("Slimed", 0): (0, 0, 0, [], [], [], True, 0, False),

        # Ironclad Cards
        ("Strike", 0): (6, 0, 1, [], [], [], False, 0, False),
        ("Defend", 0): (0, 5, 0, [], [], [], False, 0, False),
        ("Bash", 0): (8, 0, 1, [], [], [], False, 0, False),
        ("Anger", 0): (6, 0, 1, [], [], [("Anger", 2)], False, 0, False),
        # ("Armaments",0) : (0,0,0,[],[],[],True,0,False)
        ("Body Slam", 0): (0, 0, 0, [], [], [], False, 0, False),
        ("Clash", 0): (0, 0, 0, [], [], [], False, 0, False),
        ("Cleave", 0): (0, 0, 0, [], [], [], False, 0, True),
        ("Clothesline", 0): (12, 0, 1, [], [("Weakness", 2)], [], False, 0, False),
        ("Flex", 0): (0, 0, 0, [("Strength", 2), ("Strength Down", 2)], [], [], False, 0, False),
        # ("Havoc",0): (0,0,0,[],[],[],True,0,False),
        # ("Headbutt",0): (9,0,1,[],[],[],False,0,False),
        ("Heavy Blade", 0): (14, 0, 0, [], [], [], False, 0, False),
        ("Iron Wave", 0): (5, 5, 1, [], [], [], False, 0, False),
        ("Perfected Strike", 0): (6, 0, 0, [], [], [], False, 0, False),
        ("Pommel Strike", 0): (9, 0, 1, [], [], [], False, 1, False),
        ("Shrug It Off", 0): (0, 8, 0, [], [], [], False, 1, False),
        # ("Sword Boomerang",0): (3,0,3,[],[],[],False,0,False),
        ("Thunderclap", 0): (4, 0, 1, [], [("Vulnerable", 1)], [], False, 0, True),
        # ("True Grit",0): (0,7,0,[],[],[],False,0,False),
        ("Twin Strike", 0): (5, 0, 2, [], [], [], False, 0, False),
        # ("Warcry",0): (0,0,0,[],[],[],True,0,False),
        ("Wild Strike", 0): (12, 0, 1, [], [], [("Wound", 0)], False, 0, False),
        ("Battle Trance", 0): (0, 0, 0, [("No Draw", 1)], [], [], False, 3, False),
        # ("Blood for Blood",0):(18,0,1,[],[],[],False,0,False),
        ("Bloodletting", 0): (0, 0, 0, [], [], [], False, 0, False),
        # ("Burning Pact",0):(0,0,0,[],[],[],False,2,False),
        ("Carnage", 0): (20, 0, 1, [], [], [], False, 0, False),
        ("Combust", 0): (0, 0, 0, [("Combust", 5)], [], [], False, 0, False),
        ("Dark Embrace", 0): (0, 0, 0, [("Dark Embrace", 1)], [], [], False, 0, False),
        ("Disarm", 0): (0, 0, 0, [], [("Strength", -2)], [], True, 0, False),
        ("Dropkick", 0): (5, 0, 1, [], [], [], False, 0, False),
        # ("Dual Wield",0):(0,0,0,[],[],[],False,0,False),
        ("Entrench", 0): (0, 0, 0, [], [], [], False, 0, False),
        ("Evolve", 0): (0, 0, 0, [("Evolve", 1)], [], [], False, 0, False),
        ("Feel No Pain", 0): (0, 0, 0, [("Feel No Pain", 3)], [], [], False, 0, False),
        ("Fire Breathing", 0): (0, 0, 0, [("Fire Breathing", 6)], [], [], False, 0, False),
        ("Flame Barrier", 0): (0, 12, 0, [("Flame Barrier", 4)], [], [], False, 0, False),
        ("Ghostly Armor", 0): (0, 10, 0, [], [], [], False, 0, False),
        ("Hemokinesis", 0): (15, 0, 1, [], [], [], False, 0, False),
        # ("Infernal Blade",0): (0,0,0,[],[],[],True,0,False),
        ("Inflame", 0): (0, 0, 0, [("Strength", 2)], [], [], False, 0, False),
        ("Intimidate", 0): (0, 0, 0, [], [("Weakness", 1)], [], True, 0, True),
        ("Metallicize", 0): (0, 0, 0, [("Metalicize", 3)], [], [], False, 0, False),
        ("Power Through", 0): (0, 15, 0, [], [], [("Wound", 1), ("Wound", 1)], False, 0, False),
        ("Pummel", 0): (2, 0, 4, [], [], [], False, 0, False),
        ("Rage", 0): (0, 0, 0, [("Rage", 3)], [], [], False, 0, False),
        # ("Rampage") : (8,0,1,[],[],[],False,0,False)
        ("Reckless Charge", 0): (7, 0, 1, [], [], [("Dazed", 0)]),
        ("Rupture", 0): (0, 0, 0, [("Rupture", 1)], [], []),
        # ("Searing Blow",0) : (12,0,0,[],[],[],False,0,False),
        # ("Second Wind",0) : (0,5,0,[],[],[],False,0,False),
        # ("Searing Red",0) : (0,0,0,[],[],[],True,0,False),
        ("Sentinel", 0): (0, 5, 0, [], [], [], False, 0, False),
        # ("Sever Soul",0) : (16,0,1,[],[],[],False,0,False),
        ("Shockwave", 0): (0, 0, 0, [], [("Weakness", 3), ("Vulnerable", 3)], [], False, 0, True),
        # ("Spot Weakness",0): (0,0,0,[("Strength",3)],[],[],False,0,False),
        ("Uppercut", 0): (13, 0, 1, [], [("Weakness", 1), ("Vulnerable", 1)], [], False, 0, False),
        ("Whirlwind", 0): (5, 0, 0, [], [], [], False, 0, True),
        ("Barricade", 0): (0, 0, 0, [("Barricade", 1)], [], [], False, 0, False),
        ("Berserk", 0): (0, 0, 0, [("Vulnerable", 2), ("Berserk", 1)], [], [], False, 0, False),
        ("Bludgeon", 0): (32, 0, 1, [], [], [], False, 0, False),
        ("Brutality", 0): (0, 0, 0, [("Brutality", 1)], [], [], False, 0, False),
        ("Corruption", 0): (0, 0, 0, [("Corruption", 1)], [], [], False, 0, False),
        ("Demon Form", 0): (0, 0, 0, [("Demon Form", 2)], [], [], False, 0, False),
        ("Double Tap", 0): (0, 0, 0, [("Double Tap", 1)], [], [], False, 0, False),
        # ("Exhume",0):(0,0,0,[],[],[],True,0,False),
        # ("Feed",0):(10,0,0,[],[],[],True,0,False),
        ("Fiend Fire", 0): (7, 0, 0, [], [], [], True, 0, False),
        ("Immolate", 0): (21, 0, 1, [], [], [("Burn", 2)], False, 0, True),
        ("Impervious", 0): (0, 30, 0, [], [], [], True, 0, False),
        ("Juggernaut", 0): (0, 0, 0, [("Juggernaut", 5)], [], [], True, 0, False),
        ("Limit Break", 0): (0, 0, 0, [], [], [], True, 0, False),
        ("Offering", 0): (0, 0, 0, [], [], [], True, 1, False),
        ("Reaper", 0): (4, 0, 0, [], [], [], True, 0, True),

        ("Strike+", 0): (9, 0, 1, [], [], [], False, 0, False),
        ("Defend+", 0): (0, 8, 0, [], [], [], False, 0, False),
        ("Bash+", 0): (10, 0, 1, [], [("Vulnerable", 3)], [], False, 0, False),
        ("Anger+", 0): (8, 0, 1, [], [], [("Anger", 2)], False, 0, False),
        ("Armaments+", 0): (0, 0, 0, [], [], [], False, 0, True),
        # ("Body Slam+",0) : (0,0,0,[],[],[],False,0,False),
        ("Clash+", 0): (0, 0, 0, [], [], [], False, 0, False),
        ("Cleave+", 0): (0, 0, 0, [], [], [], False, 0, True),
        ("Clothesline+", 0): (14, 0, 1, [], [("Weakness", 3)], [], False, 0, False),
        ("Flex+", 0): (0, 0, 0, [("Strength", 4), ("Strength Down", 4)], [], [], False, 0, False),
        # ("Havoc+",0): (0,0,0,[],[],[],False,0,False),
        # ("Headbutt+",0): (9,0,1,[],[],[],False,0,False),
        ("Heavy Blade+", 0): (14, 0, 0, [], [], [], False, 0, False),
        ("Iron Wave+", 0): (7, 7, 1, [], [], []),
        ("Perfected Strike+", 0): (6, 0, 0, [], [], [], False, 0, False),
        ("Pommel Strike+", 0): (9, 0, 1, [], [], [], False, 2, False),
        ("Shrug It Off+", 0): (0, 11, 0, [], [], [], False, 1, False),
        # ("Sword Boomerang+",0): (3,0,3,[],[],[],False,0,False),
        ("Thunderclap+", 0): (4, 0, 1, [], [("Vulnerable", 1)], [], False, 0, True),
        # ("True Grit+",0): (0,7,0,[],[],[],False,0,False),
        ("Twin Strike+", 0): (7, 0, 2, [], [], [], False, 0, False),
        # ("Warcry+",0): (0,0,0,[],[],[],True,0,False),
        ("Wild Strike+", 0): (17, 0, 1, [], [], [("Wound", 0)], False, 0, False),
        ("Battle Trance+", 0): (0, 0, 0, [("No Draw", 1)], [], [], False, 4, False),
        ("Blood for Blood+", 0): (22, 0, 1, [], [], [], False, 0, False),
        # ("Bloodletting+",0):(0,0,0,[],[],[],False,0,False),
        # ("Burning Pact+",0):(0,0,0,[],[],[],False,3,False),
        # ("Carnage+",0) : (28,0,1,[],[],[],False,0,False),
        ("Combust+", 0): (0, 0, 0, [("Combust", 7)], [], [], False, 0, False),
        ("Dark Embrace+", 0): (0, 0, 0, [("Dark Embrace", 2)], [], [], False, 0, False),
        ("Disarm+", 0): (0, 0, 0, [], [("Strength", -3)], [], True, 0, False),
        ("Dropkick+", 0): (8, 0, 1, [], [], [], False, 0, False, False, 0, False),
        # ("Dual Wield+",0):(0,0,0,[],[],[],False,0,False),
        ("Entrench+", 0): (0, 0, 0, [], [], [], False, 0, False),
        ("Evolve+", 0): (0, 0, 0, [("Evolve", 2)], [], [], False, 0, False),
        ("Feel No Pain+", 0): (0, 0, 0, [("Feel No Pain", 4)], [], [], False, 0, False),
        ("Fire Breathing+", 0): (0, 0, 0, [("Fire Breathing", 10)], [], [], False, 0, False),
        ("Flame Barrier+", 0): (0, 16, 0, [("Flame Barrier", 6)], [], [], False, 0, False),
        ("Ghostly Armor+", 0): (0, 13, 0, [], [], [], False, 0, False),
        ("Hemokinesis+", 0): (20, 0, 1, [], [], [], False, 0, False),
        # ("Infernal Blade+",0): (0,0,0,[],[],[],True,0,False),
        ("Inflame+", 0): (0, 0, 0, [("Strength", 3)], [], [], False, 0, False),
        ("Intimidate+", 0): (0, 0, 0, [], [("Weakness", 2)], [], True, 0, True),
        ("Metallicize+", 0): (0, 0, 0, [("Metalicize", 4)], [], [], False, 0, False),
        ("Power Through+", 0): (0, 20, 0, [], [], [("Wound", 1), ("Wound", 1)], False, 0, False),
        ("Pummel+", 0): (2, 0, 5, [], [], [], False, 0, False),
        ("Rage+", 0): (0, 0, 0, [("Rage", 5)], [], [], False, 0, False),
        # ("Rampage+") : (8,0,1,[],[],[],False,0,False)
        ("Reckless Charge+", 0): (10, 0, 1, [], [], [("Dazed", 0)], False, 0, False),
        ("Rupture+", 0): (0, 0, 0, [("Rupture", 2)], [], [], False, 0, False),
        # ("Searing Blow+",0) : (16,0,0,[],[],[],False,0,False),
        # ("Second Wind+",0) : (0,5,0,[],[],[],False,0,False),
        # ("Searing Red+",0) : (0,0,0,[],[],[],True,0,False),
        ("Sentinel+", 0): (0, 8, 0, [], [], [], False, 0, False),
        # ("Sever Soul+",0) : (16,0,1,[],[],[],False,0,False),
        ("Shockwave+", 0): (0, 0, 0, [], [("Weakness", 5), ("Vulnerable", 5)], [], False, 0, True),
        # ("Spot Weakness+",0): (0,0,0,[("Strength",3)],[],[],False,0,False),
        ("Uppercut+", 0): (13, 0, 1, [], [("Weakness", 2), ("Vulnerable", 2)], [], False, 0, False),
        ("Whirlwind+", 0): (7, 0, 0, [], [], [], False, 0, True),
        ("Barricade+", 0): (0, 0, 0, [("Barricade", 1)], [], [], False, 0, False),
        ("Berserk+", 0): (0, 0, 0, [("Vulnerable", 1), ("Berserk", 1)], [], [], False, 0, False),
        ("Bludgeon+", 0): (42, 0, 1, [], [], [], False, 0, False),
        ("Brutality+", 0): (0, 0, 0, [("Brutality", 1)], [], [], False, 0, False),
        ("Corruption+", 0): (0, 0, 0, [("Corruption", 1)], [], [], False, 0, False),
        ("Demon Form+", 0): (0, 0, 0, [("Demon Form", 3)], [], [], False, 0, False),
        ("Double Tap+", 0): (0, 0, 0, [("Double Tap", 2)], [], [], False, 0, False),
        # ("Exhume+",0):(0,0,0,[],[],[],True,0,False),
        # ("Feed+",0):(10,0,0,[],[],[],True,0,False),
        ("Fiend Fire+", 0): (10, 0, 0, [], [], [], True, 0, False),
        ("Immolate+", 0): (21, 0, 1, [], [], [("Burn", 2)], False, 0, True),
        ("Impervious+", 0): (0, 40, 0, [], [], [], True, 0, False),
        ("Juggernaut+", 0): (0, 0, 0, [("Juggernaut", 7)], [], [], False, 0, False),
        ("Limit Break+", 0): (0, 0, 0, [], [], [], False, 0, False),
        ("Offering+", 0): (0, 0, 0, [], [], [], False, 1, False),
        ("Reaper+", 0): (5, 0, 0, [], [], [], True, 0, True),

        ("Apparition", 0): (0, 0, 0, [("Intangible", 1)], [], [], True, 0, False),
        ("Madness", 0): (0, 0, 0, [], [], [], True, 0, False)
    }

    added_card_data = {
        "Slimed": (-1, "Slimed", "Status", "Common", 0, False, 1, -1, "", "", True, False),
        "Wound": (-1, "Wound", "Status", "Common", 0, False, 1, -1, "", "", False, False),
        "Dazed": (-1, "Dazed", "Status", "Common", 0, False, 1, -1, "", "", False, True),
        "Burn": (-1, "Burn", "Status", "Common", 0, False, 1, -1, "", "", False, False),
        "Burn+": (-1, "Burn+", "Status", "Common", 0, False, 1, -1, "", "", False, False),

        "Anger": (-1, "Anger", "Attack", "Common", 0, True, 1, -1, "", "", True, False),
        "Anger+": (-1, "Anger+", "Attack", "Common", 0, True, 1, -1, "", "", True, False),

    }

    def __init__(self, damage, block, num_hits, s_powers, t_powers, cards, exhaust, draw_cards, aoe):
        self.damage = damage
        self.block = block

        self.num_hits = num_hits
        self.self_powers = s_powers
        # list of tuples in the format of (power, amount)
        self.target_powers = t_powers
        # list of tuples in the format of (card, place) where place is 0: deck, 1:hand, 2: discard
        self.cards = cards
        self.is_exhaust = exhaust
        self.draw_cards = draw_cards
        self.aoe = aoe

    def execute_move(self, game_state, actor: Character, target: Character, node=None, card_to_play=None, is_double_tapped=False):
        if not card_to_play is None:
            if card_to_play.type == CardType.ATTACK:
                try:
                    rage_index = [
                        i.power_name for i in actor.powers].index("Rage")
                    actor.block = actor.block + actor.powers[rage_index].amount
                except:
                    pass

        if not is_double_tapped:
            try:
                double_tap_index = [
                    i.power_name for i in actor.powers].index("Double Tap")
                if (actor.powers[double_tap_index].amount > 0):
                    actor.powers[double_tap_index].amount = actor.powers[double_tap_index].amount - 1
                    self.execute_move(game_state, actor, target,
                                      node, card_to_play, True)
            except:
                pass

        if (not target == None):
            for i in range(self.num_hits):

                if isinstance(actor, Monster):
                    if actor.name == "Shelled Parasite" and Monster_Action.id_map["Shelled Parasite"]["Suck"] == actor.move_id:
                        unblocked_damage = actor.adjust_damage(
                            self.damage, target.powers) - target.block
                        if unblocked_damage > 0:
                            actor.current_hp += unblocked_damage
                    if actor.name == "The Maw" and Monster_Action.id_map["The Maw"]["Nom"] == actor.move_id:
                        self.damage = math.ceil(game_state.turn/2)
                    if actor.name == "Transient" and Monster_Action.id_map["Transient"]["Attack"] == actor.move_id:
                        self.damage = 30 + ((game_state.turn-1) * 10)

                target.recieve_damage(game_state, actor.adjust_damage(
                    self.damage, target.powers), True)

                if isinstance(target, Monster):
                    if target.name == "The Guardian":
                        try:
                            mode_shift_index = [
                                i.power_name for i in target.powers].index("Mode Shift")
                            if target.powers[mode_shift_index].amount <= 0:
                                target.block = 20
                                target.move_id = Monster_Action.id_map[target.name]["Defensive Mode"]
                        except ValueError:
                            continue

            for power in self.target_powers:
                try:
                    index = [i.power_name for i in target.powers].index(
                        power[0])
                    target.powers[index].amount = target.powers[index].amount + power[1]

                except ValueError:
                    target.powers.append(Power(power[0], power[0], power[1]))

        if isinstance(actor, Monster):
            if actor.name == "Hexaghost" and Monster_Action.id_map["Hexaghost"]["Inferno"] == actor.move_id:
                for card in game_state.draw_pile:
                    if card.name == "Burn":
                        card.name = "Burn+"
                for card in game_state.discard_pile:
                    if card.name == "Burn":
                        card.name = "Burn+"
                for card in game_state.hand:
                    if card.name == "Burn":
                        card.name = "Burn+"

            elif actor.name == "Hexaghost" and Monster_Action.id_map["Hexaghost"]["Divider"] == actor.move_id:
                self.damage = int(game_state.current_hp / 12) + 1

            elif actor.name == "Slime Boss" and actor.current_hp <= actor.max_hp / 2:

                acid_slime = Monster(
                    "Acid Slime (L)", None, actor.current_hp, actor.current_hp, 0, None, False, False, move_id=2)
                spike_slime = Monster(
                    "Spike Slime (L)", None, actor.current_hp, actor.current_hp, 0, None, False, False, move_id=1)
                game_state.monsters.append(acid_slime)
                game_state.monsters.append(spike_slime)

                actor.current_hp = 0
                game_state.update()

            elif actor.name == "Acid Slime (L)" and actor.current_hp <= actor.max_hp / 2:

                new_slime = Monster(
                    "Acid Slime (M)", None, actor.current_hp, actor.current_hp, 0, None, False, False, move_id=2)
                game_state.monsters.append(new_slime)
                new_slime2 = copy.deepcopy(new_slime)
                game_state.monsters.append(new_slime2)

                actor.current_hp = 0
                game_state.update()

            elif actor.name == "Spike Slime (L)" and actor.current_hp <= actor.max_hp / 2:

                new_slime = Monster(
                    "Spike Slime (M)", None, actor.current_hp, actor.current_hp, 0, None, False, False, move_id=1)
                game_state.monsters.append(new_slime)
                new_slime2 = copy.deepcopy(new_slime)
                game_state.monsters.append(new_slime2)

                actor.current_hp = 0
                game_state.update()

            elif actor.name == "Centurion" and Monster_Action.id_map["Centurion"]["Defend"] == actor.move_id:
                for monster in game_state.monsters:
                    if monster != actor:
                        monster.block += 15

            elif actor.name == "Mystic":
                if Monster_Action.id_map["Mystic"]["Heal"] == actor.move_id:
                    for monster in game_state.monsters:
                        if monster.current_hp + 16 > monster.max_hp:
                            monster.current_hp = monster.max_hp
                        else:
                            monster.current_hp += 16

                if Monster_Action.id_map["Mystic"]["Buff"] == actor.move_id:
                    for monster in game_state.monsters:
                        try:
                            strength = [m.power_name for m in monster.powers].index(
                                "Strength")
                            monster.powers[strength].amount += 2
                        except ValueError:
                            monster.powers.append(
                                Power("Strength", "Strength", 2))

            elif actor.name == "Gremlin Leader":
                if Monster_Action.id_map["Gremlin Leader"]["Encourage"] == actor.move_id:
                    for monster in game_state.monsters:
                        if monster != actor:
                            monster.block += 6

                elif Monster_Action.id_map["Gremlin Leader"]["Encourage"] == actor.move_id:
                    # SUMMON RANDOM GREMLINS
                    pass

            elif actor.name == "Bronze Automaton" and Monster_Action.id_map["Bronze Automaton"]["Spawn Orbs"] == actor.move_id:
                bronze_orb = Monster("Orb", None, 58, 58,
                                     0, None, False, False, move_id=3)
                bronze_orb2 = copy.deepcopy(bronze_orb)
                game_state.monsters.append(bronze_orb)
                game_state.monsters.append(bronze_orb2)
                game_state.update()

            elif actor.name == "Orb" and Monster_Action.id_map["Orb"]["Support Beam"] == actor.move_id:
                for monster in game_state.monsters:
                    if monster.name == "Bronze Automaton":
                        monster.block += 12

            elif actor.name == "The Collector":
                if 1 == actor.move_id or 5 == actor.move_id:
                    torch_head = Monster(
                        "Torch Head", None, 40, 40, 0, None, False, False, move_id=1)
                    torch_head2 = copy.deepcopy(torch_head)
                    game_state.monsters.append(torch_head)
                    game_state.monsters.append(torch_head2)
                    game_state.update()

                elif Monster_Action.id_map["The Collector"]["Buff"] == actor.move_id:
                    for monster in game_state.monsters:
                        try:
                            strength = [m.power_name for m in monster.powers].index(
                                "Strength")
                            monster.powers[strength].amount += 3
                        except ValueError:
                            monster.powers.append(
                                Power("Strength", "Strength", 3))

            elif actor.name == "The Exploder" and Monster_Action.id_map["Exploder"]["Explode"] == actor.move_id:
                actor.current_hp = 0
                game_state.update()

            elif actor.name == "Reptomancer" and Monster_Action.id_map["Reptomancer"]["Summon"] == actor.move_id:
                dagger = Monster("Dagger", None, 25, 25, 0, None, False,
                                 False, move_id=Monster_Action.id_map["Dagger"]["Stab"])
                game_state.monsters.append(dagger)
                game_state.update()

            elif actor.name == "Dagger" and Monster_Action.id_map["Dagger"]["Explode"] == actor.move_id:
                actor.current_hp = 0
                game_state.update()

            elif actor.name == "Donu" and Monster_Action.id_map["Donu"]["Circle of Power"] == actor.move_id:
                for monster in game_state.monsters:
                    try:
                        strength = [m.power_name for m in monster.powers].index(
                            "Strength")
                        monster.powers[strength].amount += 3
                    except ValueError:
                        monster.powers.append(Power("Strength", "Strength", 3))

            elif actor.name == "Deca" and Monster_Action.id_map["Deca"]["Square of Protection"] == actor.move_id:
                for monster in game_state.monsters:
                    monster.block += 16

                    monster.powers.append(
                        Power("Strength", "Strength", 2))

        if (self.aoe):
            for target in game_state.monsters:
                for i in range(self.num_hits):
                    target.recieve_damage(game_state, actor.adjust_damage(
                        self.damage, target.powers), True)

                for power in self.target_powers:
                    try:
                        index = [i.power_name for i in target.powers].index(
                            power[0])
                        target.powers[index].amount = target.powers[index].amount + power[1]

                    except ValueError:
                        target.powers.append(
                            Power(power[0], power[0], power[1]))

        for power in self.self_powers:
            try:
                index = [i.power_name for i in actor.powers].index(
                    power[0])
                actor.powers[index].amount = actor.powers[index].amount + power[1]

            except ValueError:
                actor.powers.append(Power(power[0], power[0], power[1]))

        for card in self.cards:
            if card[1] == 0:
                game_state.draw_pile.append(
                    Card(*Move.added_card_data[card[0]]))

            if card[1] == 1:
                game_state.hand.append(Card(*Move.added_card_data[card[0]]))

            if card[1] == 2:
                game_state.discard_pile.append(
                    Card(*Move.added_card_data[card[0]]))

        actor.block = actor.block + self.block

        if not card_to_play is None:
            game_state.hand.remove(card_to_play)

            if self.is_exhaust:
                game_state.exhaust_pile.append(card_to_play)
            else:
                game_state.discard_pile.append(card_to_play)

        if not node is None:

            node.expand_on_draw(self.draw_cards, game_state)

        if not card_to_play is None:

            try:
                index = [i.power_name for i in actor.powers].index("Hex")
                for _ in range(actor.powers[index].amount):
                    game_state.draw_pile.append(
                        Card(*Move.added_card_data["Dazed"]))

            except ValueError:
                pass

            if card_to_play.name == "Armaments":
                pass  # TODO: fill this later
            if card_to_play.name == "Armaments+":
                for card in game_state.hand:
                    if not "+" in card.name and not card.name == "Burn":
                        card.name = card.name + "+"

            if card_to_play.name == "Body Slam" or card_to_play.name == "Body Slam+":
                target.recieve_damage(game_state, actor.adjust_damage(
                    actor.block, target.powers), True)

            if card_to_play.name == "Havoc" or card_to_play.name == "Havoc+":
                pass  # TODO: fill this later

            if card_to_play.name == "Headbutt" or card_to_play.name == "Headbutt+":
                pass  # TODO: fill this later

            if card_to_play.name == "Heavy Blade" or card_to_play.name == "Heavy Blade+":
                upgrade = 3
                if "+" in card_to_play.name:
                    upgrade = 5
                target.recieve_damage(game_state, actor.adjust_damage(
                    self.damage, target.powers, heavy_blade=upgrade), True)

            if card_to_play.name == "Perfected Strike" or card_to_play.name == "Perfected Strike+":
                strikes = 0
                for card in game_state.discard_pile:
                    if "strike" in card.name:
                        strikes = strikes + 1
                    if "Strike" in card.name:
                        strikes = strikes + 1

                for card in game_state.draw_pile:
                    if "strike" in card.name:
                        strikes = strikes + 1
                    if "Strike" in card.name:
                        strikes = strikes + 1

                for card in game_state.hand:
                    if "strike" in card.name:
                        strikes = strikes + 1
                    if "Strike" in card.name:
                        strikes = strikes + 1

                mult = 2
                if "+" in card_to_play.name:
                    mult = 3

                target.recieve_damage(game_state, actor.adjust_damage(
                    self.damage + mult*strikes, target.powers), True)

            if card_to_play.name == "Sword Boomerang" or card_to_play.name == "Sword Boomerang+":
                pass  # TODO: fill this later

            if card_to_play.name == "True Grit":
                pass  # TODO: fill this later

            if card_to_play.name == "True Grit+":
                pass  # TODO: fill this later

            if card_to_play.name == "Warcry" or card_to_play.name == "Warcry+":
                pass  # TODO: fill this later

            if card_to_play.name == "Bloodletting" or card_to_play.name == "Bloodletting+":
                energy_gained = 2
                if "+" in card_to_play.name:
                    energy_gained = 3

                actor.energy = actor.energy + energy_gained

                target.recieve_damage(game_state, 3, False)
            if card_to_play.name == "Burning Pact" or card_to_play.name == "Burning Pact+":
                pass  # TODO: fill this later
            if card_to_play.name == "Dropkick" or card_to_play.name == "Dropkick+":
                try:
                    index = [i.power_name for i in actor.powers].index(
                        "Vulnerable")

                    actor.energy = actor.energy + 1
                    node.expand_on_draw(1, game_state)
                except ValueError:
                    pass

            if card_to_play.name == "Dual Wield" or card_to_play.name == "Dual Wield+":
                pass  # TODO: fill this later
            if card_to_play.name == "Entrench" or card_to_play.name == "Entrench+":
                actor.block = actor.block*2
            if card_to_play.name == "Hemokinesis" or card_to_play.name == "Hemokinesis+":
                target.recieve_damage(game_state, 2, False)
            if card_to_play.name == "Infernal Blade" or card_to_play.name == "Infernal Blade+":
                pass  # TODO: fill this later
            if card_to_play.name == "Rampage" or card_to_play.name == "Rampage+":
                pass  # TODO: fill this later
            if card_to_play.name == "Searing Blow" or card_to_play.name == "Searing Blow+":
                pass  # TODO: fill this later
            if card_to_play.name == "Second Wind" or card_to_play.name == "Second Wind+":
                pass  # TODO: fill this later
            if card_to_play.name == "Searing Red" or card_to_play.name == "Searing Red+":
                pass  # TODO: fill this later
            if card_to_play.name == "Sever Soul" or card_to_play.name == "Sever Soul+":
                pass  # TODO: fill this later
            if card_to_play.name == "Shockwave" or card_to_play.name == "Shockwave+":
                pass  # TODO: fill this later
            if card_to_play.name == "Spot Weakness" or card_to_play.name == "Spot Weakness+":
                pass  # TODO: fill this later
            if card_to_play.name == "Whirlwind" or card_to_play.name == "Whirlwind+":
                for target in game_state.monsters:
                    for i in range(actor.energy):
                        target.recieve_damage(game_state, actor.adjust_damage(
                            self.damage, target.powers), True)
                actor.energy = 0
            if card_to_play.name == "Exhume" or card_to_play.name == "Exhume+":
                pass

            if card_to_play.name == "Feed" or card_to_play.name == "Feed+":
                pass  # TODO: fill this later
            if card_to_play.name == "Fiend Fire" or card_to_play.name == "Fiend Fire+":
                count = 0
                for card in game_state.hand:
                    game_state.exhaust_pile.append(card)
                    conut = count + 1

                game_state.hand.clear()
                for i in range(count):
                    target.recieve_damage(game_state, actor.adjust_damage(
                        self.damage, target.powers), True)

            if card_to_play.name == "Limit Break" or card_to_play.name == "Limit Break+":
                try:
                    index = [i.power_name for i in actor.powers].index(
                        "Strength")

                    actor.powers[index].amount = actor.powers[index].amount * 2
                except:
                    pass
            if card_to_play.name == "Reaper" or card_to_play.name == "Reaper+":
                monster_hp = sum(
                    [monster.current_hp for monster in game_state.monsters])
                for target in game_state.monsters:
                    target.recieve_damage(game_state, actor.adjust_damage(
                        self.damage, target.powers), True)
                changed_hp = monster_hp - \
                    sum([monster.current_hp for monster in game_state.monsters])
                actor.current_hp = actor.current_hp + changed_hp
