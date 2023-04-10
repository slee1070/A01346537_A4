"""
Sung Lee
A01346537
"""

from helper.print_helper import slow_print


def make_character():
    """
    Generate a dictionary that represents the player's character.

    :postcondition: the character name is set by the player
    :postcondition: the character class is set by the player
    :postcondition: the character dictionary is created with relevant attributes
    :return: a dictionary representing the character
    >>>
    """
    def get_player_class():
        slow_print("Are you a wizard or a warrior?\n1. wizard\n2. warrior")
        player_class = input()
        while player_class != "1" and player_class != "2":
            slow_print("That doesn't align with your spirit. Please choose again.\nAre you a wizard or a warrior?")
            player_class = input()

        return "wizard" if player_class == "1" else "warrior"

    def get_player_name():
        slow_print("What is your name?")
        player_name = input()
        while not player_name:
            slow_print("Please speak more clearly.\nWhat is your name?")
            player_name = input()

        return player_name

    return {
        "name": get_player_name(),
        "class": get_player_class(),
        "location": (0, 0),
        "equipment": {},
        "stats": {"level": 1, "attack": 2, "current_hp": 10, "max_hp": 10, "victories": 0},
        "gold": 30,
        "flags": {
            "atk_boosted": False,
            "hp_boosted": False,
            "achieved_goal": False
        }
    }


def get_attack_strength(character):
    """
    Calculate the attack strength of the character from base attack and items.

    :param character: a dictionary representing the player
    :precondition: character is a dictionary that has the stats and attack keys and an integer value
    :precondition: character is a dictionary that has the equipment key and a list of items as value
    :postcondition: attack items, if any, are added to the character base attack value
    :return: an integer representing the total attack value
    >>>
    """
    strength = character["stats"]["attack"]
    for equipment in character["equipment"]:
        attributes = character["equipment"][equipment]
        if attributes["bonus"]["stat"] == "attack":
            strength += attributes["bonus"]["amount"]
    return strength


def get_max_hp(character):
    """
    Calculate the hp of the character from base hp and items.

    :param character: a dictionary representing the player
    :precondition: character is a dictionary that has the stats and max_hp keys and an integer value
    :precondition: character is a dictionary that has the equipment key and a list of items as value
    :postcondition: hp items, if any, are added to the character base hp value
    :return: an integer representing the total hp value
    >>>
    """
    hp = character["stats"]["max_hp"]
    for item in character["equipment"].values():
        if item["bonus"]["stat"] == "hp":
            hp += item["bonus"]["amount"]
    return hp


def move_character(character: dict, direction: str) -> bool:
    """
    Update the character's location with the target direction.

    :param character: a dictionary representing the player
    :param direction: a string representing the direction to move
    :precondition: character is a dictionary with the keys location and value is a tuple of x and y coordinates
    :precondition: direction is a string that is up, down, left, or right
    :postcondition: the character location is updated according to the direction
    :return: True if the location is updated, otherwise False
    >>>
    """
    moved = True
    character_coordinate = character["location"]
    if direction == "up":
        slow_print("You go up...")
        character["location"] = (character_coordinate[0], character_coordinate[1] + 1)
    elif direction == "down":
        slow_print("You go down...")
        character["location"] = (character_coordinate[0], character_coordinate[1] - 1)
    elif direction == "left":
        slow_print("You go left...")
        character["location"] = (character_coordinate[0] - 1, character_coordinate[1])
    elif direction == "right":
        slow_print("You go right...")
        character["location"] = (character_coordinate[0] + 1, character_coordinate[1])
    else:
        moved = False
    return moved


def still_alive(character: dict) -> bool:
    """
    Determine if a character is alive.

    :param character: a dictionary representing the player or a monster
    :precondition: the character is a dictionary that has the keys stats and current_hp with an integer value
    :postcondition: the value of current_hp is checked to see if it is greater than 0
    :return: True of current_hp is greater than 0, otherwise False
    >>>
    """
    return character["stats"]["current_hp"] > 0


def inspect_self(character: dict) -> None:
    """
    Display information about the player's character.

    :param character: a dictionary representing the player
    :precondition: character is a dictionary with valid keys
    :postcondition: certain information about the character is printed to the player
    >>>
    """
    slow_print("You look at yourself in the mirror...")
    print(f"Name: {character['name']}")
    print(f"Level: {character['stats']['level']}")
    print(f"Class: {character['class']}")
    print(f"Equipped: {[item for item in character['equipment']]}")
    print(f"Attack: {get_attack_strength(character)}")
    print(f"HP: {character['stats']['current_hp']}/{get_max_hp(character)}")
    print(f"Wallet: {character['gold']} gold")


def check_for_level_up(character: dict) -> None:
    """
    Level up the character if qualified.

    :param character: a dictionary representing the player
    :precondition: character must be a dictionary with the keys stats and victories with an integer value
    :precondition: character must be a dictionary with the keys stats and level with an integer value
    :postcondition: if victories is twice the value of level, then increase the attack, max_hp and level
    :postcondition: if victories is twice the value of level, then set victories to 0
    >>>
    """
    fights = character["stats"]["victories"]
    level = character["stats"]["level"]
    if fights == level * 2:
        character["stats"]["level"] += 1
        character["stats"]["victories"] = 0
        slow_print(f"You have levelled up! You are now level {character['stats']['level']}")
        character["stats"]["attack"] += level * 5
        character["stats"]["max_hp"] += level * 15
        character["stats"]["current_hp"] = character["stats"]["max_hp"]
