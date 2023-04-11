"""
Sung Lee
A01346537
"""

import random

from character.character import still_alive, check_for_level_up, get_attack_strength
from character.monster import generate_boss
from helper import VOWELS
from helper.helper import slow_print, get_user_choice


def describe_monsters(monsters: list) -> str:
    """
    Generate a description of the monsters in the current battle.

    :param monsters: a list of dictionaries representing the monsters
    :precondition: monsters is a non-empty list of dictionaries
    :postcondition: a string is generated describing the monsters in the current battle
    :return: a string describing the monsters in the current battle
    :raises: ValueError: if monsters is an empty list
    >>> describe_monsters([{"monster": "Dragon", "stats": {"attack": 5, "max_hp": 20, "current_hp": 20}, "gold": 1, \
    "equipment": []}, {"monster": "Goblin", "stats": {"attack": 3, "max_hp": 10, "current_hp": 10}, "gold": 2, \
    "equipment": []}])
    'You spot a Dragon and a Goblin!'
    """
    text = "You spot "
    for number, monster in enumerate(monsters, 0):
        if monster["monster"][0] in VOWELS:
            text += f"an {monster['monster']}"
        else:
            text += f"a {monster['monster']}"
        if number < len(monsters) - 2 and len(monsters) - 2 >= 0:
            text += ", "
        elif number < len(monsters) - 1:
            text += " and "
    text += "!"
    return text


def calculate_damage(attacker: dict) -> int:
    """
    Calculate the damage that the attacker can inflict.

    :param attacker: a dictionary that represents the attacking entity
    :precondition: attacker must have an attack value greater than 0
    :postcondition: the amount of damage inflicted is calculated based on the attacker's strength and the dice roll
    :return: an integer representing the damage inflicted
    :raises: ValueError: if attacker's attack value is less than or equal to 0
    """
    damage = get_attack_strength(attacker)
    dice_result = random.randint(1, 20)
    slow_print(f"..and rolled {dice_result}!")

    def process_dice_result(strength):
        if dice_result == 20:
            slow_print("CRITICAL HIT!")
            strength *= 2
        elif dice_result == 1:
            slow_print("Missed!")
            strength *= 0
        elif 1 < dice_result <= 5:
            slow_print("A weak blow!")
            strength -= strength // 2
        elif 15 <= dice_result <= 19:
            slow_print("A strong blow!")
            strength += strength // 2
        else:
            slow_print("Hit!")
        return strength

    return process_dice_result(damage)


def player_attacks(character: dict, monsters: list) -> None:
    """
    Inflict damage on a monster with a player attack.

    :param character: a dictionary representing the player
    :param monsters: a list of dictionaries representing the monsters
    :precondition: character must have a valid class and attack value greater than 0
    :precondition: monsters must have at least 1 monster
    :postcondition: damage is inflicted on the first monster in the list, the monster's hp is updated,
                    and the monster is removed from the list if its hp is 0 or less
    :return: None
    """
    monster = monsters[0]
    if character["class"] == "warrior":
        slow_print("You swing your longsword!")
    else:
        slow_print("You cast a sizzling beam of energy!")

    slow_print("You roll a d20")
    damage = calculate_damage(character)

    slow_print(f"You deal {damage} damage to the {monster['monster']}.")
    monster["stats"]["current_hp"] -= damage
    if not still_alive(monster):
        slow_print(f"You've slayed the {monster['monster']}!")
        monsters.remove(monster)


def monsters_attack(character: dict, monsters: list) -> None:
    """
    Simulate the attack of each monster in the list against the character.

    :param character: a dictionary representing the player's character
    :param monsters: a list of dictionaries representing the monsters
    :precondition: character must be a dictionary
    :precondition: monsters must be a list of dictionaries
    :postcondition: the monsters' attack is resolved and the player's health is updated accordingly
    :return: None
    """
    for monster in monsters:
        slow_print(f"The {monster['monster']} attacks...")
        slow_print(f"The {monster['monster']} roll a d20")
        damage = calculate_damage(monster)

        slow_print(f"It deals {damage} damage to you.")
        character["stats"]["current_hp"] -= damage
        if not still_alive(character):
            print("You died!")
            return


def determine_sneak(character: dict, monsters: list) -> int:
    """
    Determine if the player can sneak up on the monster(s) and attack first.

    :param character: a dictionary representing the player
    :param monsters: a list of dictionaries representing the monsters
    :precondition: character must be a dictionary
    :precondition: monsters must be a list of dictionaries
    :postcondition: determines whether the player can sneak up on the monster(s) and attack first
    :return: turn counter as an integer
    """
    turn_counter = 1
    initiative = random.randint(1, 10)
    if initiative == 1:
        print(f"\n== TURN {turn_counter} == ")
        slow_print(f"You sneak up on the monster{'s' if len(monsters) > 1 else ''}!")
        player_attacks(character, monsters)
        print(f"== END OF TURN ==")
        turn_counter += 1
    else:
        slow_print("Combat begins!")
    return turn_counter


def gain_rewards(character: dict, gold: int) -> None:
    """
    Adds the specified amount of gold to the character's inventory and increments the victory counter

    :param character: a dictionary representing the player character
    :param gold: an integer representing the amount of gold to be added
    :precondition: character must be a dictionary with valid keys and values
    :precondition: gold must be a positive integer
    :postcondition: the specified amount of gold is added to the character's gold inventory and
                    the victory counter is incremented
    :return: None
    >>> test_character = {'name': 'John', 'class': 'warrior', 'stats': \
    {'max_hp': 50, 'current_hp': 50, 'level': 1, 'experience': 0, 'victories': 0}, 'gold': 0, 'equipment': []}
    >>> gain_rewards(test_character, 50)
    <BLANKLINE>
    You are victorious!
    You found 50 gold.
    >>> print(test_character['gold'])
    50
    """
    slow_print("\nYou are victorious!")
    slow_print(f"You found {gold} gold.")
    character["gold"] += gold
    character["stats"]["victories"] += 1
    check_for_level_up(character)


def enter_combat(character: dict, monsters: list) -> bool:
    """
    Enter combat between the player and monsters.

    :param character: a dictionary representing the player
    :param monsters: a list of dictionaries representing the monsters
    :precondition: character must be a dictionary
    :precondition: monsters must be a list of dictionaries
    :postcondition: a combat sequence is initiated and resolved according to game rules
    :return: a boolean value representing whether the player won or lost the combat
    """
    turn_counter = determine_sneak(character, monsters)
    while still_alive(character) and len(monsters) > 0:
        slow_print(f"\n== TURN {turn_counter} == ")
        slow_print(f"You are fighting: {', '.join([monster['monster'] for monster in monsters])}")
        slow_print(f"You have {character['stats']['current_hp']} hp")
        turn_counter += 1
        if not continue_attack():
            flee_combat(character, monsters)
            return False
        player_attacks(character, monsters)
        monsters_attack(character, monsters)
        print(f"== END OF TURN ==")
    return True


def continue_attack() -> bool:
    """
    Determine whether the player wants to continue attacking or run away.

    :postcondition: returns a boolean value indicating whether to continue attacking (True) or to run away (False)
    :return: a boolean value indicating whether to continue attacking (True) or to run away (False)
    """
    attack = True
    options = [("fight", f" 1: Attack"), ("run", f" 2: Run")]
    choice = get_user_choice(options, "What would you like to do?\n")
    if choice == "run":
        attack = False
    return attack


def flee_combat(character: dict, monsters: list) -> None:
    """
    Allow the player to attempt to flee from combat.

    :param character: a dictionary representing the player
    :param monsters: a list of dictionaries representing the monsters in the combat encounter
    :precondition: character must be a dictionary
    :precondition: monsters must be a list of dictionaries
    :return: None
    >>> test_character = {"name": "Calico", "stats": {"current_hp": 20, "max_hp": 20}}
    >>> test_monsters = [{"monster": "Goblin", "stats": {"attack": 5, "current_hp": 10, "max_hp": 10}}]
    >>> flee_combat(test_character, test_monsters)
    You successfully fled but the Goblin hits you for 5 damage
    >>> test_character["stats"]["current_hp"]
    15
    """
    monster = random.choice(monsters)
    damage = monster["stats"]["attack"]
    slow_print(f"You successfully fled but the {monster['monster']} hits you for {damage} damage")
    character["stats"]["current_hp"] -= damage


def initialize_combat(character: dict, monsters: list, gold: int) -> None:
    """
    Begin a combat encounter between the player and a group of monsters.

    :param character: a dictionary representing the player
    :param monsters: a list of dictionaries representing the monsters
    :param gold: an integer representing the gold that can be gained by the player if they win the combat
    :precondition: character must be a dictionary
    :precondition: monsters must be a list of dictionaries
    :precondition: gold must be a positive integer
    :precondition: the character dictionary must have a "name" key with a non-empty string value
                   and a "stats" key with a dictionary value containing "current_hp" and
                   "max_hp" keys with integer values representing the player's current and maximum HP respectively
    :precondition: the monsters list must contain at least one dictionary with "monster"  and "stats" keys, where
                   the "stats" dictionary should have "attack", "defense", "max_hp", and "current_hp" keys with
                   integer values representing the monster's attack, defense, maximum and current HP respectively
    :postcondition: if the player wins the combat, their gold amount will increase by the specified amount
    :return: None
    """
    victorious = enter_combat(character, monsters)
    if victorious and still_alive(character):
        gain_rewards(character, gold)


def initialize_boss_fight(character: dict) -> bool:
    """
    Initiate the boss fight by generating a boss monster and entering combat.

    :param character: a dictionary representing the player
    :precondition: character must be a dictionary that has a "name" key with a non-empty string value
                   and a "stats" key with a dictionary value containing "current_hp" and "max_hp" keys with
                   integer values representing the player's current and maximum HP respectively
    :postcondition: character's flags dictionary will have an "achieved_goal" key with a boolean value
                    indicating if the player has defeated the boss or not
    :return: a boolean value indicating if the player has achieved the goal or not
    """
    monsters, gold = generate_boss(character)
    victorious = enter_combat(character, monsters)
    if victorious and still_alive(character):
        gain_rewards(character, gold)
        slow_print("You've done it! You've defeated the evil cat!")
        character["flags"]["achieved_goal"] = True
    return True
