MONSTER_LIST = {
    1: ["kobold", "goblin", "skeleton", "zombie", "giant rat", "stirge", "bandit", "orc", "imp"],
    2: ["banshee", "basilisk", "bugbear", "chimera", "ettin", "gargoyle", "gelatinous cube", "manticore"],
    3: ["beholder", "lich", "dragon", "tarrasque", "balor", "pit fiend"]
}

MONSTER_STATS = {
    1: {
        "min_hp": 1,
        "max_hp": 5,
        "min_atk": 1,
        "max_atk": 3
    },
    2: {
        "min_hp": 4,
        "max_hp": 12,
        "min_atk": 4,
        "max_atk": 6
    },
    3: {
        "min_hp": 8,
        "max_hp": 20,
        "min_atk": 6,
        "max_atk": 8
    },
    "boss": {
        "min_hp": 25,
        "max_hp": 30,
        "min_atk": 7,
        "max_atk": 10
    }
}
