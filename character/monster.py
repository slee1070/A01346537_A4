"""
Sung Lee
A01346537
"""

import random

from character import MONSTER_STATS, MONSTER_LIST


def generate_monsters(character: dict) -> tuple:
    """
    Generate a list of monsters and gold for the player to encounter in a dungeon.

    :param character: A dictionary representing the player character
    :precondition: character must be a dictionary
    :precondition: character must have a "stats" key which contains a dictionary of the player's stats,
                   including "level"
    :postcondition: Returns a tuple containing a list of dictionaries representing the monsters in
                    the dungeon, and the amount of gold the player can collect by defeating the monsters
    :return: A tuple containing a list of dictionaries representing the monsters in the dungeon, and the
             amount of gold the player can collect by defeating the monsters
    """
    level = character["stats"]["level"]
    monsters = [generate_monster(tier) for tier in range(1, level + 1)]
    gold = 0
    for monster in monsters:
        gold += monster["gold"]
    return monsters, gold


def generate_boss(character: dict) -> tuple:
    """
    Generate a boss monster and add it to the list of generated monsters using the `generate_monsters` function.

    :param character: a dictionary representing the player
    :precondition: character must be a dictionary
    :precondition: character must contain a "stats" key containing a dictionary with a "level" key
    :postcondition: returns a tuple containing the list of generated monsters and the amount of gold
    :return: A tuple containing the list of generated monsters and the amount of gold
    """
    stats = MONSTER_STATS["boss"]
    hp = random.randint(stats["min_hp"], stats["max_hp"])
    boss = {
        "monster": "Purrsecutor",
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
    """
    Generate a random monster of a given tier.

    :param tier: an integer representing the tier of the monster
    :precondition: tier must be an integer between 1 and 3, inclusive
    :postcondition: returns a dictionary representing the generated monster
    :return: a dictionary with the following keys:
             - "monster": a string representing the name of the monster
             - "stats": a dictionary with the following keys:
                         - "attack": an integer representing the attack power of the monster
                         - "max_hp": an integer representing the maximum hp of the monster
                         - "current_hp": an integer representing the current hp of the monster
             - "gold": an integer representing the amount of gold dropped by the monster
             - "equipment": an empty list
    :raises ValueError: if tier is not an integer between 1 and 3, inclusive
    """
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
