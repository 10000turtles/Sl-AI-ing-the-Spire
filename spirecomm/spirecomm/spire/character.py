from enum import Enum
import random

from spirecomm.spire.power import Power


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
        "Jaw Worm": {
            "Chomp": 1, "Bellow": 2, "Thrash": 3
        }, "Red Louse": {
            "Bite": 1, "Grow": 2
        }, "Green Louse": {
            "Bite": 1, "Spit Web": 2
        }, "Cultist": {
            "Incantation": 1, "Dark Strike": 2
        }, "Acid Slime (M)": {
            "Corrosive Spit": 1, "Lick": 2, "Tackle": 3
        }, "Spike Slime (M)": {
            "Flame Tackle": 1, "Lick": 2
        }, "Acid Slime (S)": {
            "Lick": 1, "Tackle": 2
        }, "Spike Slime (S)": {
            "Tackle": 1
        }
    }

    def __init__(self, intent, power, probability):

        self.intent = None
        self.power = None
        self.probability = None

        



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

    def adjust_damage(self, base_power, target_powers):
        try:
            index = [i.power_name for i in self.powers].index("Strength")
            return base_power + self.powers[index].amount
        except ValueError:
            return base_power


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
        self.move = Move(*Move.monster_move_data[(self.name, self.move_id)])

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

    def possible_intents(self):

        intents = []
        if self.name == "Jaw Worm":
            chomp = Monster_Action.id_map[self.name]["Chomp"]
            bellow = Monster_Action.id_map[self.name]["Bellow"]
            thrash = Monster_Action.id_map[self.name]["Trash"]

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
        elif self.name == "Red Louse":
            d = random.randrange(5,7)
            bite = Monster_Action.id_map[self.name]["Bite"]
            grow = Monster_Action.id_map[self.name]["Grow"]
            if self.last_move_id == self.second_last_move_id:
                if self.last_move_id == bite:
                    intents.append(Monster_Action(grow, 0, 1))
                elif self.last_move_id == grow:
                    intents.append(Monster_Action(bite, d, 1))
            else:
                intents.append(Monster_Action(bite, d, 3/4))
                intents.append(Monster_Action(grow, 0, 1/4))
        elif self.name == "Green Louse":
            d = random.randrange(5,7)
            bite = Monster_Action.id_map[self.name]["Bite"]
            spit_web = Monster_Action.id_map[self.name]["Spit Web"]
            if self.last_move_id == self.second_last_move_id:
                if self.last_move_id == bite:
                    intents.append(Monster_Action(spit_web, 0, 1))
                elif self.last_move_id == spit_web:
                    intents.append(Monster_Action(bite, d, 1))
            else:
                intents.append(Monster_Action(bite, d, 3/4))
                intents.append(Monster_Action(spit_web, 0, 1/4))

        return intents

    def __eq__(self, other):
        if(other == None):
            return False
        if self.name == other.name and self.current_hp == other.current_hp and self.max_hp == other.max_hp and self.block == other.block:
            if len(self.powers) == len(other.powers):
                for i in range(len(self.powers)):
                    if self.powers[i] != other.powers[i]:
                        return False
                return True
        return False


class Move:

    # data format: (monster name, moveid) : (damage, block, strength, self powers, target powers, cards added to deck)
    monster_move_data = {
        ("Jaw Worm", Monster_Action.id_map["Jaw Worm"]["Chomp"]): (0, 6, 0, [("Strength", 3)], [], []),
        ("Jaw Worm", Monster_Action.id_map["Jaw Worm"]["Bellow"]): (11, 0, 1, [], [], []),
        ("Jaw Worm", Monster_Action.id_map["Jaw Worm"]["Thrash"]): (7, 5, 1, [], [], []),

        ("Red Louse", Monster_Action.id_map["Red Louse"]["Bite"]): ('d', 0, 0, [], [], []),
        ("Red Louse", Monster_Action.id_map["Red Louse"]["Grow"]): (0, 0, 0, [("Strength", 3)], [], []),

        ("Green Louse", Monster_Action.id_map["Green Louse"]["Bite"]): ('d', 0, 0, [], [], []),
        ("Green Louse", Monster_Action.id_map["Green Louse"]["Spit Web"]): (0, 0, 0, [], [("Weak", 2)], []),

        ("Cultist", Monster_Action.id_map["Cultist"]["Incantation"]): (0, 0, 0, [("Ritual", 3)], [], []),
        ("Cultist", Monster_Action.id_map["Cultist"]["Dark Strike"]): (6, 0, 0, [], [], []),

        ("Acid Slime (M)", Monster_Action.id_map["Acid Slime (M)"]["Corrosive Spit"]): (7, 0, 0, [], [], [("Slimed", 1)]),
        ("Acid Slime (M)", Monster_Action.id_map["Acid Slime (M)"]["Lick"]): (0, 0, 0, [], [("Weak", 1)], []),
        ("Acid Slime (M)", Monster_Action.id_map["Acid Slime (M)"]["Tackle"]): (10, 0, 0, [], [], []),

        ("Spiked Slime (M)", Monster_Action.id_map["Spiked Slime (M)"]["Flame Tackle"]): (8, 0, 0, [], [], [("Slimed", 1)]),
        ("Spiked Slime (M)", Monster_Action.id_map["Spiked Slime (M)"]["Lick"]): (0, 0, 0, [], [("Frail", 1)], []),

        ("Acid Slime (S)", Monster_Action.id_map["Acid Slime (S)"]["Lick"]): (0, 0, 0, [], [("Weak", 1)], []),
        ("Acid Slime (S)", Monster_Action.id_map["Acid Slime (S)"]["Tackle"]): (3, 0, 0, [], [], []),

        ("Spiked Slime (S)", Monster_Action.id_map["Spiked Slime (S)"]["Tackle"]): (5, 0, 0, [], [], []),




        # Ironclad Cards
        ("Strike", 0): (6, 0, 1, [], [], []),
        ("Defend", 0): (0, 5, 0, [], [], []),
        ("Bash", 0): (8, 0, 1, [], [], []),
        ("Anger", 0): (6, 0, 1, [], [], [("Anger", 2)]),
        # ("Armaments",0) : (0,0,0,[],[],[])
        # ("Body Slam",0) : (0,0,0,[],[],[])
        # ("Clash",0) : (0,0,0,[],[],[])
        # ("Cleave",0) : (0,0,0,[],[],[])
        ("Clothesline", 0): (12, 0, 1, [], [("Weakness", 2)], []),
        ("Flex", 0): (0, 0, 0, [("Strength", 2), ("Strength Down", 2)], [], []),
        # ("Havoc",0): (0,0,0,[],[],[]),
        # ("Headbutt",0): (9,0,1,[],[],[]),
        # ("Heavy Blade",0): (14,0,1,[],[],[]),
        ("Iron Wave", 0): (5, 5, 1, [], [], []),
        # ("Perfected Strike",0): (6,0,1,[],[],[]),
        # ("Pommel Strike",0): (9,0,1,[],[],[]),
        # ("Shrug It Off",0): (0,8,0,[],[],[]),
        # ("Sword Boomerang",0): (3,0,3,[],[],[]),
        # ("Thunderclap",0): (4,0,1,[],[("Vulnerable",1)],[]),
        # ("True Grit",0): (0,7,0,[],[],[]),
        ("Twin Strike", 0): (5, 0, 2, [], [], []),
        # ("Warcry",0): (0,0,0,[],[],[]),
        ("Wild Strike", 0): (12, 0, 1, [], [], [("Wound", 0)]),
        # ("Battle Trance",0):(0,0,0,[],[],[]),
        # ("Blood for Blood",0):(18,0,1,[],[],[]),
        # ("Bloodletting",0):(0,0,0,[],[],[]),
        # ("Burning Pact",0):(0,0,0,[],[],[]),
        # ("Carnage",0) : (20,0,1,[],[],[]),
        ("Combust", 0): (0, 0, 0, [("Combust", 5)], [], []),
        ("Dark Embrace", 0): (0, 0, 0, [("Dark Embrace", 1)], [], []),
        ("Disarm", 0): (0, 0, 0, [], [("Strength", -2)], []),
        # ("Dropkick",0):(5,0,1,[],[],[]),
        # ("Dual Wield",0):(0,0,0,[],[],[]),
        # ("Entrench",0) : (0,0,0,[],[],[]),
        ("Evolve", 0): (0, 0, 0, [("Evolve", 1)], [], []),
        ("Feel No Pain", 0): (0, 0, 0, [("Feel No Pain", 3)], [], []),
        ("Fire Breathing", 0): (0, 0, 0, [("Fire Breathing", 6)], [], []),
        ("Flame Barrier", 0): (0, 0, 0, [("Flame Barrier", 4)], [], []),
        ("Ghostly Armor", 0): (0, 10, 0, [], [], []),
        ("Hemokinesis", 0): (15, 0, 1, [], [], []),
        # ("Infernal Blade",0): (0,0,0,[],[],[]),
        ("Inflame", 0): (0, 0, 0, [("Strength", 2)], [], []),
        # ("Intimidate",0):(0,0,0,[],[("Weakness",1)],[])
        ("Metallicize", 0): (0, 0, 0, [("Metalicize", 3)], [], []),
        ("Power Through", 0): (0, 15, 0, [], [], [("Wound", 1), ("Wound", 1)]),
        ("Pummel", 0): (2, 0, 4, [], [], []),
        ("Rage", 0): (0, 0, 0, [("Rage", 3)], [], []),
        # ("Rampage") : (8,0,1,[],[],[])
        ("Reckless Charge", 0): (7, 0, 1, [], [], [("Dazed", 0)]),
        ("Rupture", 0): (0, 0, 0, [("Rupture", 1)], [], []),
        # ("Searing Blow",0) : (12,0,0,[],[],[]),
        # ("Second Wind",0) : (0,5,0,[],[],[]),
        # ("Searing Red",0) : (0,0,0,[],[],[]),
        ("Sentinel", 0): (0, 5, 0, [], [], []),
        # ("Sever Soul",0) : (16,0,1,[],[],[]),
        # ("Shockwave",0) : (0,0,0,[],[("Weakness",3),("Vulnerable",3)],[]),
        # ("Spot Weakness",0): (0,0,0,[("Strength",3)],[],[]),
        ("Uppercut", 0): (13, 0, 1, [], [("Weakness", 1), ("Vulnerable", 1)], []),
        # ("Whirlwind",0) : (5,0,X,[],[],[]),
        ("Barricade", 0): (0, 0, 0, [("Barricade", 1)], [], []),
        ("Berserk", 0): (0, 0, 0, [("Vulnerable", 2), ("Berserk", 1)], [], []),
        ("Bludgeon", 0): (32, 0, 1, [], [], []),
        ("Brutality", 0): (0, 0, 0, [("Brutality", 1)], [], []),
        ("Corruption", 0): (0, 0, 0, [("Corruption", 1)], [], []),
        ("Demon Form", 0): (0, 0, 0, [("Demon Form", 2)], [], []),
        ("Double Tap", 0): (0, 0, 0, [("Double Tap", 1)], [], []),
        # ("Exhume",0):(0,0,0,[],[],[]),
        # ("Feed",0):(10,0,0,[],[],[]),
        # ("Fiend Fire",0):(7,0,X,[],[],[]),
        # ("Immolate",0) : (21,0,1,[],[],[("Burn",2)]),
        # ("Impervious",0): (0,30,0,[],[],[]),
        ("Juggernaut", 0): (0, 0, 0, [("Juggernaut", 5)], [], []),
        # ("Limit Break",0): (0,0,0,[],[],[]),
        # ("Offering",0): (0,0,0,[],[],[]),
        # ("Reaper",0): (4,0,0,[],[],[])

        ("Strike", 0): (6, 0, 1, [], [], []),
        ("Defend", 0): (0, 5, 0, [], [], []),
        ("Bash", 0): (8, 0, 1, [], [], []),
        ("Anger", 0): (6, 0, 1, [], [], [("Anger", 2)]),
        # ("Armaments",0) : (0,0,0,[],[],[])
        # ("Body Slam",0) : (0,0,0,[],[],[])
        # ("Clash",0) : (0,0,0,[],[],[])
        # ("Cleave",0) : (0,0,0,[],[],[])
        ("Clothesline", 0): (12, 0, 1, [], [("Weakness", 2)], []),
        ("Flex", 0): (0, 0, 0, [("Strength", 2), ("Strength Down", 2)], [], []),
        # ("Havoc",0): (0,0,0,[],[],[]),
        # ("Headbutt",0): (9,0,1,[],[],[]),
        # ("Heavy Blade",0): (14,0,1,[],[],[]),
        ("Iron Wave", 0): (5, 5, 1, [], [], []),
        # ("Perfected Strike",0): (6,0,1,[],[],[]),
        # ("Pommel Strike",0): (9,0,1,[],[],[]),
        # ("Shrug It Off",0): (0,8,0,[],[],[]),
        # ("Sword Boomerang",0): (3,0,3,[],[],[]),
        # ("Thunderclap",0): (4,0,1,[],[("Vulnerable",1)],[]),
        # ("True Grit",0): (0,7,0,[],[],[]),
        ("Twin Strike", 0): (5, 0, 2, [], [], []),
        # ("Warcry",0): (0,0,0,[],[],[]),
        ("Wild Strike", 0): (12, 0, 1, [], [], [("Wound", 0)]),
        # ("Battle Trance",0):(0,0,0,[],[],[]),
        # ("Blood for Blood",0):(18,0,1,[],[],[]),
        # ("Bloodletting",0):(0,0,0,[],[],[]),
        # ("Burning Pact",0):(0,0,0,[],[],[]),
        # ("Carnage",0) : (20,0,1,[],[],[]),
        ("Combust", 0): (0, 0, 0, [("Combust", 5)], [], []),
        ("Dark Embrace", 0): (0, 0, 0, [("Dark Embrace", 1)], [], []),
        ("Disarm", 0): (0, 0, 0, [], [("Strength", -2)], []),
        # ("Dropkick",0):(5,0,1,[],[],[]),
        # ("Dual Wield",0):(0,0,0,[],[],[]),
        # ("Entrench",0) : (0,0,0,[],[],[]),
        ("Evolve", 0): (0, 0, 0, [("Evolve", 1)], [], []),
        ("Feel No Pain", 0): (0, 0, 0, [("Feel No Pain", 3)], [], []),
        ("Fire Breathing", 0): (0, 0, 0, [("Fire Breathing", 6)], [], []),
        ("Flame Barrier", 0): (0, 0, 0, [("Flame Barrier", 4)], [], []),
        ("Ghostly Armor", 0): (0, 10, 0, [], [], []),
        ("Hemokinesis", 0): (15, 0, 1, [], [], []),
        # ("Infernal Blade",0): (0,0,0,[],[],[]),
        ("Inflame", 0): (0, 0, 0, [("Strength", 2)], [], []),
        # ("Intimidate",0):(0,0,0,[],[("Weakness",1)],[])
        ("Metallicize", 0): (0, 0, 0, [("Metalicize", 3)], [], []),
        ("Power Through", 0): (0, 15, 0, [], [], [("Wound", 1), ("Wound", 1)]),
        ("Pummel", 0): (2, 0, 4, [], [], []),
        ("Rage", 0): (0, 0, 0, [("Rage", 3)], [], []),
        # ("Rampage") : (8,0,1,[],[],[])
        ("Reckless Charge", 0): (7, 0, 1, [], [], [("Dazed", 0)]),
        ("Rupture", 0): (0, 0, 0, [("Rupture", 1)], [], []),
        # ("Searing Blow",0) : (12,0,0,[],[],[]),
        # ("Second Wind",0) : (0,5,0,[],[],[]),
        # ("Searing Red",0) : (0,0,0,[],[],[]),
        ("Sentinel", 0): (0, 5, 0, [], [], []),
        # ("Sever Soul",0) : (16,0,1,[],[],[]),
        # ("Shockwave",0) : (0,0,0,[],[("Weakness",3),("Vulnerable",3)],[]),
        # ("Spot Weakness",0): (0,0,0,[("Strength",3)],[],[]),
        ("Uppercut", 0): (13, 0, 1, [], [("Weakness", 1), ("Vulnerable", 1)], []),
        # ("Whirlwind",0) : (5,0,X,[],[],[]),
        ("Barricade", 0): (0, 0, 0, [("Barricade", 1)], [], []),
        ("Berserk", 0): (0, 0, 0, [("Vulnerable", 2), ("Berserk", 1)], [], []),
        ("Bludgeon", 0): (32, 0, 1, [], [], []),
        ("Brutality", 0): (0, 0, 0, [("Brutality", 1)], [], []),
        ("Corruption", 0): (0, 0, 0, [("Corruption", 1)], [], []),
        ("Demon Form", 0): (0, 0, 0, [("Demon Form", 2)], [], []),
        ("Double Tap", 0): (0, 0, 0, [("Double Tap", 1)], [], []),
        # ("Exhume",0):(0,0,0,[],[],[]),
        # ("Feed",0):(10,0,0,[],[],[]),
        # ("Fiend Fire",0):(7,0,X,[],[],[]),
        # ("Immolate",0) : (21,0,1,[],[],[("Burn",2)]),
        # ("Impervious",0): (0,30,0,[],[],[]),
        ("Juggernaut", 0): (0, 0, 0, [("Juggernaut", 5)], [], []),
        # ("Limit Break",0): (0,0,0,[],[],[]),
        # ("Offering",0): (0,0,0,[],[],[]),
        # ("Reaper",0): (4,0,0,[],[],[])
    }

    def __init__(self, damage, block, num_hits, s_powers, t_powers, cards):
        self.damage = damage
        self.block = block

        self.num_hits = num_hits
        self.self_powers = s_powers
        # list of tuples in the format of (power, amount)
        self.target_powers = t_powers
        # list of tuples in the format of (card, place) where place is 0: deck, 1:hand, 2: discard
        self.cards = cards

    def execute_move(self, gameState, actor: Character, target: Character):

        if (not target == None):
            for i in range(self.num_hits):
                if target.block < actor.adjust_damage(self.damage, target.powers):
                    target.current_hp = target.current_hp - \
                        (actor.adjust_damage(self.damage, target.powers) - target.block)
                    target.block = 0
                else:
                    target.block = target.block - \
                        actor.adjust_damage(self.damage, target.powers)

            for power in self.self_powers:
                try:
                    index = [i.power_name for i in actor.powers].index(
                        power[0])
                    actor.powers[index].amount = actor.powers[index].amount + power[1]

                except ValueError:
                    actor.powers.append(Power(power[0], power[0], power[1]))

            for power in self.target_powers:
                try:
                    index = [i.power_name for i in target.powers].index(
                        power[0])
                    target.powers[index].amount = target.powers[index].amount + power[1]

                except ValueError:
                    target.powers.append(Power(power[0], power[0], power[1]))

        actor.block = actor.block + self.block
