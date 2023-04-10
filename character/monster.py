"""
Sung Lee
A01346537
"""

import random

from character import MONSTER_STATS, MONSTER_LIST


def generate_monsters(character: dict) -> tuple:
    level = character["stats"]["level"]
    monsters = [generate_monster(tier) for tier in range(1, level + 1)]
    gold = 0
    for monster in monsters:
        gold += monster["gold"]
    return monsters, gold


def generate_boss(character: dict) -> tuple:
    stats = MONSTER_STATS["boss"]
    hp = random.randint(stats["min_hp"], stats["max_hp"])
    boss = {
        "monster": "Big Bad Evil Cat",
        "stats": {
            "attack": random.randint(stats["min_atk"], stats["max_atk"]),
            "max_hp": hp,
            "current_hp": hp
        },
        "gold": 0,
        "equipment": []
    }
    monsters, gold = generate_monsters(character)
    monsters.append(boss)
    return monsters, gold


def generate_monster(tier) -> dict:
    if tier > 3:
        if tier % 3 == 0:
            tier = 3
        else:
            tier = tier % 3
    stats = MONSTER_STATS[tier]
    hp = random.randint(stats["min_hp"], stats["max_hp"])
    return {
        "monster": random.choice(MONSTER_LIST[tier]),
        "stats": {
            "attack": random.randint(stats["min_atk"], stats["max_atk"]),
            "max_hp": hp,
            "current_hp": hp
        },
        "gold": random.randint(1, tier) * tier * 3,
        "equipment": []
    }
