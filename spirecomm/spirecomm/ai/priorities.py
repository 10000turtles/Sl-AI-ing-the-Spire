import math


class Priority:

    CARD_PRIORITY_LIST = []

    PLAY_PRIORITY_LIST = []

    AOE_CARDS = []

    DEFENSIVE_CARDS = []

    MAX_COPIES = {}

    BOSS_RELIC_PRIORITY_LIST = []

    MAP_NODE_PRIORITIES_1 = {'R': 1000, 'E': 10,
                             '$': 100, '?': 100, 'M': 1, 'T': 0}

    MAP_NODE_PRIORITIES_2 = {'R': 1000, 'E': 100,
                             '$': 10, '?': 10, 'M': 1, 'T': 0}

    MAP_NODE_PRIORITIES_3 = {'R': 1000, 'E': 1,
                             '$': 100, '?': 100, 'M': 10, 'T': 0}

    GOOD_CARD_ACTIONS = [
        "PutOnDeckAction",
        "ArmamentsAction",
        "DualWieldAction",
        "NightmareAction",
        "RetainCardsAction",
        "SetupAction"
    ]

    BAD_CARD_ACTIONS = [
        "DiscardAction",
        "ExhaustAction",
        "PutOnBottomOfDeckAction",
        "RecycleAction",
        "ForethoughtAction",
        "GamblingChipAction"
    ]

    def __init__(self):
        self.CARD_PRIORITIES = {
            self.CARD_PRIORITY_LIST[i]: i for i in range(len(self.CARD_PRIORITY_LIST))}
        self.PLAY_PRIORITIES = {
            self.PLAY_PRIORITY_LIST[i]: i for i in range(len(self.PLAY_PRIORITY_LIST))}
        self.BOSS_RELIC_PRIORITIES = {self.BOSS_RELIC_PRIORITY_LIST[i]: i for i in range(
            len(self.BOSS_RELIC_PRIORITY_LIST))}
        self.MAP_NODE_PRIORITIES = {
            1: self.MAP_NODE_PRIORITIES_1,
            2: self.MAP_NODE_PRIORITIES_2,
            3: self.MAP_NODE_PRIORITIES_3,
            4: self.MAP_NODE_PRIORITIES_3  # Doesn't really matter anyway
        }

    def get_best_card(self, card_list):
        return min(card_list, key=lambda x: self.CARD_PRIORITIES.get(x.card_id, math.inf) - 0.5 * x.upgrades)

    def get_worst_card(self, card_list):
        return max(card_list, key=lambda x: self.CARD_PRIORITIES.get(x.card_id, math.inf) - 0.5 * x.upgrades)

    def get_sorted_cards(self, card_list, reverse=False):
        return sorted(card_list, key=lambda x: self.CARD_PRIORITIES.get(x.card_id, math.inf) - 0.5 * x.upgrades, reverse=reverse)

    def get_sorted_cards_to_play(self, card_list, reverse=False):
        return sorted(card_list, key=lambda x: self.PLAY_PRIORITIES.get(x.card_id, math.inf) - 0.5 * x.upgrades, reverse=reverse)

    def get_best_card_to_play(self, card_list):
        return min(card_list, key=lambda x: self.PLAY_PRIORITIES.get(x.card_id, math.inf) - 0.5 * x.upgrades)

    def get_worst_card_to_play(self, card_list):
        return max(card_list, key=lambda x: self.PLAY_PRIORITIES.get(x.card_id, math.inf) - 0.5 * x.upgrades)

    def should_skip(self, card):
        return self.CARD_PRIORITIES.get(card.card_id, math.inf) > self.CARD_PRIORITIES.get("Skip")

    def needs_more_copies(self, card, num_copies):
        return self.MAX_COPIES.get(card.card_id, 0) > num_copies

    def get_best_boss_relic(self, relic_list):
        return min(relic_list, key=lambda x: self.BOSS_RELIC_PRIORITIES.get(x.name, 0))

    def is_card_aoe(self, card):
        return card.card_id in self.AOE_CARDS

    def is_card_defensive(self, card):
        return card.card_id in self.DEFENSIVE_CARDS

    def get_cards_for_action(self, action, cards, max_cards):
        if action in self.GOOD_CARD_ACTIONS:
            sorted_cards = self.get_sorted_cards(cards, reverse=False)
        else:
            sorted_cards = self.get_sorted_cards(cards, reverse=True)
        num_cards = min(max_cards, len(cards))
        return sorted_cards[:num_cards]


class SilentPriority(Priority):

    CARD_PRIORITY_LIST = [
        "Footwork",
        "After Image",
        "Noxious Fumes",
        "Crippling Poison",
        "Apotheosis",
        "A Thousand Cuts",
        "Adrenaline",
        "Malaise",
        "Caltrops",
        "Corpse Explosion",
        "Dagger Spray",
        "PiercingWail",
        "Neutralize",
        "Survivor",
        "Well Laid Plans",
        "Backflip",
        "Dodge and Roll",
        "Infinite Blades",
        "Leg Sweep",
        "Backstab",
        "Glass Knife",
        "Dash",
        "J.A.X.",
        "Master of Strategy",
        "Escape Plan",
        "Cloak And Dagger",
        "Die Die Die",
        "Blur",
        "Deadly Poison",
        "Predator",
        "Deflect",
        "Flying Knee",
        "Skip",
        "Shiv",
        "Trip",
        "Good Instincts",
        "Burst",
        "Dark Shackles",
        "Terror",
        "Discovery",
        "Bane",
        "Deep Breath",
        "Violence",
        "Panache",
        "All Out Attack",
        "Catalyst",
        "Sucker Punch",
        "Secret Technique",
        "Bouncing Flask",
        "Poisoned Stab",
        "Envenom",
        "Impatience",
        "The Bomb",
        "Blind",
        "Mayhem",
        "HandOfGreed",
        "RitualDagger",
        "Bandage Up",
        "Bite",
        "Quick Slash",
        "Calculated Gamble",
        "Acrobatics",
        "Endless Agony",
        "Dagger Throw",
        "Bullet Time",
        "Flash of Steel",
        "Outmaneuver",
        "Tools of the Trade",
        "Chrysalis",
        "Finesse",
        "Ghostly",
        "Defend_G",
        "Expertise",
        "Panacea",
        "Doppelganger",
        "Skewer",
        "Slice",
        "Blade Dance",
        "Swift Strike",
        "Thinking Ahead",
        "Dramatic Entrance",
        "Madness",
        "Strike_G",
        "Phantasmal Killer",
        "Heel Hook",
        "Magnetism",
        "Finisher",
        "Flechettes",
        "Prepared",
        "Secret Weapon",
        "Distraction",
        "Metamorphosis",
        "PanicButton",
        "Night Terror",
        "Enlightenment",
        "Sadistic Nature",
        "Unload",
        "Choke",
        "Masterful Stab",
        "Transmutation",
        "Accuracy",
        "Purity",
        "Concentrate",
        "Underhanded Strike",
        "Jack Of All Trades",
        "Wraith Form v2",
        "Storm of Steel",
        "Eviscerate",
        "Riddle With Holes",
        "Setup",
        "Venomology",
        "Mind Blast",
        "Tactician",
        "Forethought",
        "Reflex",
        "Grand Finale",
        "Dazed",
        "Void",
        "AscendersBane",
        "Necronomicurse",
        "Slimed",
        "Wound",
        "Burn",
        "Clumsy",
        "Parasite",
        "Injury",
        "Shame",
        "Decay",
        "Writhe",
        "Doubt",
        "Regret",
        "Pain",
        "Normality",
        "Pride",
    ]

    DEFENSIVE_CARDS = [
        "Cloak and Dagger",
        "Leg Sweep",
        "Deflect",
        "Blur",
        "Escape Plan",
        "Survivor",
        "Defend_G",
        "Backflip",
        "PiercingWail",
        "Dodge and Roll",
        "Dark Shackles",
        "PanicButton",
        "Finesse",
        "Good Instincts"
    ]

    PLAY_PRIORITY_LIST = [
        "Apotheosis",
        "After Image",
        "Footwork",
        "Well Laid Plans",
        "A Thousand Cuts",
        "Noxious Fumes",
        "Caltrops",
        "Infinite Blades",
        "Crippling Poison",
        "Adrenaline",
        "Neutralize",
        "Glass Knife",
        "Madness",
        "Dash",
        "Backflip",
        "Blur",
        "Malaise",
        "Dagger Spray",
        "Corpse Explosion",
        "Leg Sweep",
        "Deadly Poison",
        "Dodge and Roll",
        "Survivor",
        "PiercingWail",
        "Backstab",
        "J.A.X.",
        "Master of Strategy",
        "Escape Plan",
        "Cloak And Dagger",
        "Die Die Die",
        "Predator",
        "Flying Knee",
        "Shiv",
        "Trip",
        "Good Instincts",
        "Burst",
        "Dark Shackles",
        "Terror",
        "Discovery",
        "Bane",
        "Deep Breath",
        "Violence",
        "Panache",
        "All Out Attack",
        "Deflect",
        "Sucker Punch",
        "Secret Technique",
        "Bouncing Flask",
        "Poisoned Stab",
        "Envenom",
        "Impatience",
        "The Bomb",
        "Blind",
        "Mayhem",
        "HandOfGreed",
        "RitualDagger",
        "Bandage Up",
        "Bite",
        "Quick Slash",
        "Calculated Gamble",
        "Acrobatics",
        "Endless Agony",
        "Catalyst",
        "Dagger Throw",
        "Bullet Time",
        "Flash of Steel",
        "Outmaneuver",
        "Tools of the Trade",
        "Chrysalis",
        "Finesse",
        "Ghostly",
        "Defend_G",
        "Expertise",
        "Panacea",
        "Doppelganger",
        "Skewer",
        "Slice",
        "Blade Dance",
        "Swift Strike",
        "Thinking Ahead",
        "Dramatic Entrance",
        "Strike_G",
        "Phantasmal Killer",
        "Heel Hook",
        "Magnetism",
        "Finisher",
        "Flechettes",
        "Prepared",
        "Secret Weapon",
        "Distraction",
        "Metamorphosis",
        "PanicButton",
        "Night Terror",
        "Enlightenment",
        "Sadistic Nature",
        "Unload",
        "Choke",
        "Masterful Stab",
        "Transmutation",
        "Accuracy",
        "Purity",
        "Concentrate",
        "Underhanded Strike",
        "Jack Of All Trades",
        "Wraith Form v2",
        "Storm of Steel",
        "Eviscerate",
        "Riddle With Holes",
        "Setup",
        "Venomology",
        "Mind Blast",
        "Tactician",
        "Forethought",
        "Reflex",
        "Grand Finale",
        "Dazed",
        "Void",
        "AscendersBane",
        "Necronomicurse",
        "Slimed",
        "Wound",
        "Burn",
        "Clumsy",
        "Parasite",
        "Injury",
        "Shame",
        "Decay",
        "Writhe",
        "Doubt",
        "Regret",
        "Pain",
        "Normality",
        "Pride",

    ]

    AOE_CARDS = [
        "Dagger Spray",
        "Die Die Die",
        "Crippling Poison",
        "All Out Attack"
    ]

    MAX_COPIES = {
        "Corpse Explosion": 1,
        "Footwork": 3,
        "After Image": 99,
        "Noxious Fumes": 2,
        "Crippling Poison": 1,
        "Apotheosis": 1,
        "Adrenaline": 99,
        "Malaise": 1,
        "Caltrops": 2,
        "Dagger Spray": 1,
        "PiercingWail": 2,
        "Neutralize": 1,
        "Survivor": 1,
        "Well Laid Plans": 1,
        "Backflip": 3,
        "Dodge and Roll": 1,
        "A Thousand Cuts": 1,
        "Infinite Blades": 1,
        "Leg Sweep": 2,
        "Dash": 1,
        "Flying Knee": 1,
        "J.A.X.": 1,
        "Master of Strategy": 99,
        "Escape Plan": 99,
        "Cloak And Dagger": 2,
        "Die Die Die": 2,
        "Blur": 3,
        "Deadly Poison": 1,
        "Predator": 1,
        "Deflect": 1,
        "Backstab": 2,
        "Glass Knife": 1,
    }

    BOSS_RELIC_PRIORITY_LIST = [
        "Sozu",
        "Philosopher's Stone",
        "Runic Dome",
        "Cursed Key",
        "Fusion Hammer",
        "Ectoplasm",
        "Velvet Choker",
        "Busted Crown",
        "Empty Cage",
        "Astrolabe",
        "Runic Pyramid",
        "Snecko Eye",
        "Pandora's Box",
        "Ring of the Serpent",
        "Lizard Tail",
        "Eternal Feather",
        "Coffee Dripper",
        "Tiny House",
        "Black Star",
        "Orrery",
        "Runic Cube",
        "WristBlade",
        "HoveringKite",
        "White Beast Statue",
        "Calling Bell",
    ]


class IroncladPriority(Priority):

    CARD_PRIORITY_LIST = [
        "Apotheosis",
        "Ghostly",
        "Perfected Strike",
        "Whirlwind",
        "Battle Trance",
        "Demon Form",
        "Rage",
        "Offering",
        "Impervious",
        "Immolate",
        "Limit Break",
        "Flame Barrier",
        "Master of Strategy",
        "Inflame",
        "Disarm",
        "Shrug It Off",
        "Double Tap",
        "Thunderclap",
        "Metallicize",
        "Pommel Strike",
        "Shockwave",
        "Uppercut",
        "J.A.X.",
        "PanicButton",
        "Flash of Steel",
        "Flex",
        "Anger",
        "Skip",
        "Secret Weapon",
        "Finesse",
        "Mayhem",
        "Panache",
        "Secret Technique",
        "Metamorphosis",
        "Thinking Ahead",
        "Madness",
        "Discovery",
        "Chrysalis",
        "Deep Breath",
        "Trip",
        "Enlightenment",
        "Heavy Blade",
        "Feed",
        "Fiend Fire",
        "Twin Strike",
        "Headbutt",
        "Seeing Red",
        "Combust",
        "Clash",
        "Dark Shackles",
        "Sword Boomerang",
        "Dramatic Entrance",
        "Bludgeon",
        "HandOfGreed",
        "Evolve",
        "Violence",
        "Bite",
        "Carnage",
        "Clothesline",
        "Bash",
        "Bandage Up",
        "Panacea",
        "Reckless Charge",
        "Infernal Blade",
        "Spot Weakness",
        "Strike_R",
        "Shiv",
        "Havoc",
        "RitualDagger",
        "Dropkick",
        "Feel No Pain",
        "Swift Strike",
        "Corruption",
        "Magnetism",
        "Bloodletting",
        "Iron Wave",
        "Armaments",
        "Mind Blast",
        "AscendersBane",
        "Dazed",
        "Void",
        "Rampage",
        "Ghostly Armor",
        "True Grit",
        "Blind",
        "Good Instincts",
        "Pummel",
        "Hemokinesis",
        "Exhume",
        "Reaper",
        "Cleave",
        "Warcry",
        "Purity",
        "Dual Wield",
        "Wild Strike",
        "Defend_R",
        "Body Slam",
        "Sever Soul",
        "Burning Pact",
        "Brutality",
        "Barricade",
        "Intimidate",
        "Juggernaut",
        "Sadistic Nature",
        "Dark Embrace",
        "Power Through",
        "Transmutation",
        "Sentinel",
        "Rupture",
        "Slimed",
        "Fire Breathing",
        "Second Wind",
        "Impatience",
        "The Bomb",
        "Jack Of All Trades",
        "Searing Blow",
        "Blood for Blood",
        "Berserk",
        "Entrench",
        "Forethought",
        "Clumsy",
        "Parasite",
        "Shame",
        "Injury",
        "Wound",
        "Writhe",
        "Doubt",
        "Burn",
        "Decay",
        "Regret",
        "Necronomicurse",
        "Pain",
        "Normality",
        "Pride"
    ]

    DEFENSIVE_CARDS = [
        "Power Through",
        "True Grit",
        "Impervious",
        "Shrug It Off",
        "Flame Barrier",
        "Entrench",
        "Defend_R",
        "Sentinel",
        "Second Wind",
        "Ghostly Armor",
        "Dark Shackles",
        "PanicButton",
        "Rage"
    ]

    PLAY_PRIORITY_LIST = [
        "Apotheosis",
        "Offering",
        "Demon Form",
        "Inflame",
        "Metallicize",
        "Disarm",
        "Shockwave",
        "Ghostly",
        "Limit Break",
        "Double Tap",
        "Thunderclap",
        "Immolate",
        "Uppercut",
        "Flame Barrier",
        "Shrug It Off",
        "Impervious",
        "Madness",
        "Perfected Strike",
        "Battle Trance",
        "Rage",
        "Master of Strategy",
        "Pommel Strike",
        "J.A.X.",
        "Flash of Steel",
        "Flex",
        "Anger",
        "Defend_R",
        "Bash",
        "Whirlwind",
        "PanicButton",
        "Secret Weapon",
        "Finesse",
        "Mayhem",
        "Panache",
        "Secret Technique",
        "Metamorphosis",
        "Thinking Ahead",
        "Discovery",
        "Chrysalis",
        "Deep Breath",
        "Trip",
        "Enlightenment",
        "Heavy Blade",
        "Feed",
        "Fiend Fire",
        "Twin Strike",
        "Headbutt",
        "Seeing Red",
        "Combust",
        "Clash",
        "Dark Shackles",
        "Sword Boomerang",
        "Dramatic Entrance",
        "Bludgeon",
        "HandOfGreed",
        "Evolve",
        "Violence",
        "Bite",
        "Carnage",
        "Clothesline",
        "Bandage Up",
        "Panacea",
        "Reckless Charge",
        "Infernal Blade",
        "Strike_R",
        "Spot Weakness",
        "Strike_R",
        "Shiv",
        "Havoc",
        "RitualDagger",
        "Dropkick",
        "Feel No Pain",
        "Swift Strike",
        "Corruption",
        "Magnetism",
        "Bloodletting",
        "Iron Wave",
        "Armaments",
        "Mind Blast",
        "AscendersBane",
        "Dazed",
        "Void",
        "Rampage",
        "Ghostly Armor",
        "True Grit",
        "Blind",
        "Good Instincts",
        "Pummel",
        "Hemokinesis",
        "Exhume",
        "Reaper",
        "Cleave",
        "Warcry",
        "Purity",
        "Dual Wield",
        "Wild Strike",
        "Body Slam",
        "Sever Soul",
        "Burning Pact",
        "Brutality",
        "Barricade",
        "Intimidate",
        "Juggernaut",
        "Sadistic Nature",
        "Dark Embrace",
        "Power Through",
        "Transmutation",
        "Sentinel",
        "Rupture",
        "Slimed",
        "Fire Breathing",
        "Second Wind",
        "Impatience",
        "The Bomb",
        "Jack Of All Trades",
        "Searing Blow",
        "Blood for Blood",
        "Berserk",
        "Entrench",
        "Forethought",
        "Clumsy",
        "Parasite",
        "Shame",
        "Injury",
        "Wound",
        "Writhe",
        "Doubt",
        "Burn",
        "Decay",
        "Regret",
        "Necronomicurse",
        "Pain",
        "Normality",
        "Pride"
    ]

    AOE_CARDS = [
        "Cleave",
        "Immolate",
        "Thunderclap",
        "Whirlwind"
    ]

    MAX_COPIES = {
        "Offering": 1,
        "Impervious": 99,
        "Apotheosis": 1,
        # "Ghostly": 99,
        "Perfected Strike": 99,
        "Whirlwind": 2,
        # "Battle Trance": 2,
        # "Demon Form": 1,
        "Immolate": 1,
        "Rage": 2,
        "Limit Break": 3,
        "Flame Barrier": 4,
        "Master of Strategy": 99,
        "Inflame": 1,
        "Disarm": 4,
        "Shrug It Off": 3,
        "Double Tap": 1,
        "Thunderclap": 1,
        "Fiend Fire": 2,
        "Shockwave": 1,
        "Uppercut": 1,
        "Carnage": 1,
        "Feel No Pain": 1,
        # "J.A.X.": 1,
        # "PanicButton": 1,
        "Twin Strike": 5,
        "Pommel Strike": 5,
        "Wild Strike": 3,
        "Hemokinesis": 1,
        "Metallicize": 3,
        "Reaper": 4,
        "Bludgeon": 2,
    }

    BOSS_RELIC_PRIORITY_LIST = [
        "Snecko Eye",
        "Sozu",
        "Philosopher's Stone",
        "Runic Pyramid",
        "Black Star",
        "Cursed Key",
        "Fusion Hammer",
        "Velvet Choker",
        "Busted Crown",
        "Mark of Pain",
        "Coffee Dripper",
        "Black Blood",
        "Tiny House",
        "Runic Cube",
        "Pandora's Box",
        "Calling Bell",
        "Ectoplasm",
        "Sacred Bark",
        "Astrolabe",
        "Empty Cage",
        "Runic Dome",
    ]


class DefectPowerPriority(Priority):

    CARD_PRIORITY_LIST = [
        "Echo Form",
        "Electrodynamics",
        "Defragment",
        "Biased Cognition",
        "Glacier",
        "Self Repair",
        "Apotheosis",
        "Machine Learning",
        "Static Discharge",
        "Loop",
        "Buffer",
        "Capacitor",
        "Ball Lightning",
        "Cold Snap",
        "Undo",  # Equilibrium
        "Creative AI",
        "Conserve Battery",
        "Steam",  # Steam Barrier
        "Compile Driver",
        "Reinforced Body",
        "White Noise",
        "Force Field",
        "Chill",
        "Core Surge",
        "Rainbow",
        "Streamline",
        "Turbo",
        "Coolheaded",
        "Zap",
        "Dualcast",
        "BootSequence",
        "Leap",
        "Dark Shackles",
        "PanicButton",
        "RitualDagger",
        "Panache",
        "Master of Strategy",
        "Amplify",
        "Skip",
        "Storm",
        "Heatsinks",
        "Consume",
        "Seek",
        "Discovery",
        "Finesse",
        "Magnetism",
        "Blind",
        "Thunder Strike",
        "Sunder",
        "Reboot",
        "All For One",
        "Hologram",
        "Bite",
        "Deep Breath",
        "Tempest",
        "Sweeping Beam",
        "Trip",
        "Steam Power",  # Overclock
        "Dramatic Entrance",
        "Impatience",
        "The Bomb",
        "Bandage Up",
        "Secret Technique",
        "Violence",
        "Mayhem",
        "HandOfGreed",
        "Flash of Steel",
        "Genetic Algorithm",
        "Go for the Eyes",
        "Metamorphosis",
        "Doom and Gloom",
        "Ghostly",
        "Good Instincts",
        "Thinking Ahead",
        "Defend_B",
        "Madness",
        "J.A.X.",
        "Swift Strike",
        "Secret Weapon",
        "Multi-Cast",
        "Double Energy",
        "Auto Shields",
        "Chaos",
        "Jack Of All Trades",
        "FTL",
        "Lockon",
        "Melter",
        "Panacea",
        "Gash",  # Claw
        "Rip and Tear",
        "Barrage",
        "Hyperbeam",
        "Strike_B",
        "Mind Blast",
        "Sadistic Nature",
        "Meteor Strike",
        "Fusion",
        "Skim",
        "Fission",
        "Darkness",
        "Recycle",
        "Scrape",
        "Beam Cell",
        "Shiv",
        "Redo",  # Recursion
        "Hello World",
        "Stack",
        "Reprogram",
        "Enlightenment",
        "Transmutation",
        "Chrysalis",
        "Purity",
        "Rebound",
        "Aggregate",
        "Blizzard",
        "Forethought",
        "Void",
        "Dazed",
        "AscendersBane",
        "Clumsy",
        "Necronomicurse",
        "Slimed",
        "Wound",
        "Burn",
        "Parasite",
        "Injury",
        "Shame",
        "Doubt",
        "Writhe",
        "Decay",
        "Regret",
        "Pain",
        "Pride",
        "Normality",
    ]

    MAX_COPIES = {
        "Echo Form": 2,
        "Electrodynamics": 2,
        "Defragment": 10,
        "Glacier": 3,
        "Self Repair": 1,
        "Apotheosis": 1,
        "Machine Learning": 1,
        "Static Discharge": 2,
        "Loop": 3,
        "Buffer": 2,
        "Capacitor": 2,
        "Ball Lightning": 2,
        "Cold Snap": 2,
        "Undo": 2,  # Equilibrium
        "Amplify": 2,
        "Creative AI": 1,
        "Conserve Battery": 3,
        "Compile Driver": 2,
        "Reinforced Body": 1,
        "White Noise": 1,
        "Force Field": 1,
        "Chill": 1,
        "Core Surge": 1,
        "Rainbow": 1,
        "Streamline": 1,
        "Turbo": 1,
        "Coolheaded": 3,
        "Zap": 1,
        "Dualcast": 1,
        "BootSequence": 1,
        "Leap": 1,
        "Dark Shackles": 1,
        "PanicButton": 1,
        "RitualDagger": 1,
        "Panache": 1,
        "Master of Strategy": 5,
        "Steam": 2
    }

    AOE_CARDS = [
        "Electrodynamics"
    ]

    DEFENSIVE_CARDS = [
        "Genetic Algorithm",
        "Steam",
        "Glacier",
        "Stack",
        "BootSequence",
        "Coolheaded",
        "Force Field",
        "Reinforced Body",
        "Conserve Battery",
        "Defend_B",
        "Auto Shields",
        "Hologram",
        "Leap",
        "PanicButton",
        "Dark Shackles",
        "Finesse",
        "Good Instincts",
        "Turbo",
    ]

    BOSS_RELIC_PRIORITY_LIST = [
        "Sozu",
        "Snecko Eye",
        "Philosopher's Stone",
        "Nuclear Battery",
        "Runic Dome",
        "Cursed Key",
        "Fusion Hammer",
        "Velvet Choker",
        "Ectoplasm",
        "Busted Crown",
        "Inserter",
        "Empty Cage",
        "Astrolabe",
        "Runic Pyramid",
        "Lizard Tail",
        "Eternal Feather",
        "Coffee Dripper",
        "Tiny House",
        "Black Star",
        "Orrery",
        "Pandora's Box",
        "White Beast Statue",
        "Calling Bell",
        "FrozenCore",
    ]

    PLAY_PRIORITY_LIST = [
        "Apotheosis",
        "Double Energy",
        "Amplify",
        "Echo Form",
        "Electrodynamics",
        "Defragment",
        "Storm",
        "Glacier",
        "Self Repair",
        "Machine Learning",
        "Static Discharge",
        "Loop",
        "White Noise",
        "Madness",
        "Buffer",
        "Capacitor",
        "Core Surge",
        "Biased Cognition",
        "Ball Lightning",
        "Cold Snap",
        "Undo",  # Equilibrium
        "Creative AI",
        "Conserve Battery",
        "Steam",  # Steam Barrier
        "Steam Power",
        "Compile Driver",
        "Reinforced Body",
        "Seek",
        "Force Field",
        "Chill",
        "Rainbow",
        "Streamline",
        "Turbo",
        "Coolheaded",
        "Consume",
        "Zap",
        "Dualcast",
        "BootSequence",
        "Heatsinks",
        "Leap",
        "Dark Shackles",
        "PanicButton",
        "RitualDagger",
        "Panache",
        "Master of Strategy",
        "Skip",
        "Discovery",
        "Finesse",
        "Magnetism",
        "Blind",
        "Thunder Strike",
        "Sunder",
        "All For One",
        "Hologram",
        "Bite",
        "Deep Breath",
        "Tempest",
        "Sweeping Beam",
        "Trip",
        "Dramatic Entrance",
        "Impatience",
        "The Bomb",
        "Bandage Up",
        "Secret Technique",
        "Violence",
        "Mayhem",
        "HandOfGreed",
        "Flash of Steel",
        "Reboot",
        "Genetic Algorithm",
        "Go for the Eyes",
        "Metamorphosis",
        "Doom and Gloom",
        "Ghostly",
        "Good Instincts",
        "Thinking Ahead",
        "Defend_B",
        "J.A.X.",
        "Swift Strike",
        "Secret Weapon",
        "Multi-Cast",
        "Auto Shields",
        "Chaos",
        "Jack Of All Trades",
        "FTL",
        "Lockon",
        "Melter",
        "Panacea",
        "Gash",  # Claw
        "Rip and Tear",
        "Barrage",
        "Hyperbeam",
        "Strike_B",
        "Mind Blast",
        "Sadistic Nature",
        "Meteor Strike",
        "Fusion",
        "Skim",
        "Fission",
        "Darkness",
        "Recycle",
        "Scrape",
        "Beam Cell",
        "Shiv",
        "Redo",  # Recursion
        "Hello World",
        "Stack",
        "Reprogram",
        "Enlightenment",
        "Transmutation",
        "Chrysalis",
        "Purity",
        "Rebound",
        "Aggregate",
        "Blizzard",
        "Forethought",
        "Void",
        "Dazed",
        "AscendersBane",
        "Clumsy",
        "Necronomicurse",
        "Slimed",
        "Wound",
        "Burn",
        "Parasite",
        "Injury",
        "Shame",
        "Doubt",
        "Writhe",
        "Decay",
        "Regret",
        "Pain",
        "Pride",
        "Normality",
    ]

    MAP_NODE_PRIORITIES_1 = {'R': 1000, 'E': 100,
                             '$': 10, '?': 10, 'M': 1, 'T': 0}

    MAP_NODE_PRIORITIES_2 = {'R': 100, 'E': -
                             1000, '$': 10, '?': 10, 'M': 1, 'T': 0}

    MAP_NODE_PRIORITIES_3 = {'R': 1000, 'E': 10,
                             '$': 100, '?': 100, 'M': 1, 'T': 0}
