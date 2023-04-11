"""
Sung Lee
A01346537
"""

import itertools
import random

from time import sleep
from board.board import has_boss, make_board
from board.shop import enter_shop
from character.character import move_character, inspect_self, make_character, still_alive, get_max_hp
from character.monster import generate_monsters
from combat.combat import initialize_combat, initialize_boss_fight, describe_monsters, flee_combat
from helper import INTERACTIONS, DIRECTIONS
from helper.helper import slow_print, get_user_choice, save_to_file, read_from_file


def describe_current_location(board: dict, character: dict) -> None:
    """
    Print the description of the current location of the player.

    :param board: a dictionary representing the game board
    :param character: a dictionary representing the player
    :precondition: board must be a dictionary
    :precondition: character must be a dictionary
    :postcondition: prints the description of the player's current location
    :return: None
    """
    current_coordinates = character["location"]
    current_location = board[current_coordinates]
    slow_print(f"\nYou are currently in {current_location['description']}. Your coordinates: {current_coordinates}")


def get_valid_directions(board: dict, character: dict) -> list:
    """
    Return a list of valid directions for the player's next move on the game board.

    :param board: a dictionary representing the game board
    :param character: a dictionary representing the player
    :return: a list of valid directions, which are any combination of "up", "down", "left", and "right"
    :raises: TypeError if board or character is not a dictionary
    >>> test_board = {"dimensions": {"columns": 4, "rows": 4}}
    >>> test_character = {"location": [2, 2]}
    >>> get_valid_directions(test_board, test_character)
    ['up', 'down', 'left', 'right']
    """
    choices = DIRECTIONS.copy()
    character_coordinate = character["location"]
    if character_coordinate[0] == 0:
        choices.remove("left")
    elif character_coordinate[0] == board["dimensions"]["columns"] - 1:
        choices.remove("right")

    if character_coordinate[1] == 0:
        choices.remove("down")
    elif character_coordinate[1] == board["dimensions"]["rows"] - 1:
        choices.remove("up")
    return choices


def determine_choices(board: dict, character: dict, rested: bool) -> list:
    """
    Return a list of valid choices that a player can make given the current state of the game.

    :param board: a dictionary that represents the game board
    :param character: a dictionary representing the player
    :param rested: a boolean indicating whether the player has already rested
    :precondition: board must be a dictionary
    :precondition: board must contain valid data, including dimensions and location of NPCs and items
    :precondition: character must be a dictionary
    :precondition: character must have a "name" key with a non-empty string value, a "stats" key
                   with a dictionary value containing "current_hp" and "max_hp" keys with integer values
                   representing the player's current and maximum HP respectively, and a "location" key
                   representing the player's current position on the board
    :precondition: rested must be a boolean
    :precondition: rested must indicate whether the player has already rested
    :postcondition: returns a list of tuples, where each tuple contains a choice and a corresponding description
    :return: a list of tuples, where each tuple contains a choice and a corresponding description
    >>> test_board = {"dimensions": {"rows": 5, "columns": 5}, "npcs": {(2, 2): {"npc": {"name": "Bob"}}}}
    >>> test_character = {"location": (2, 3)}
    >>> test_rested = False
    >>> determine_choices(test_board, test_character, test_rested) # doctest: +NORMALIZE_WHITESPACE
    [('up', ' 1: Go up'), ('down', ' 2: Go down'), ('left', ' 3: Go left'), ('right', ' 4: Go right'),
    ('inspect', ' 5: Inspect yourself'), ('rest', ' 6: Rest and recover your health')]
    """
    character_coordinate = character["location"]
    directions = get_valid_directions(board, character)
    choices = [(pair[1], f" {pair[0]}: Go {pair[1]}") for pair in zip(itertools.count(1), directions)]
    npc_present = character_coordinate in board["npcs"]
    if npc_present:
        if has_boss(board, character_coordinate):
            choices.append(("boss", f" {len(choices) + 1}: Start final fight with Purrsecutor"))
        else:
            choices.append(("npc", f" {len(choices) + 1}: Talk to {board[character_coordinate]['npc']['name']}"))
    choices.append(("inspect", f" {len(choices) + 1}: Inspect yourself"))
    if not rested:
        choices.append(("rest", f" {len(choices) + 1}: Rest and recover your health"))
    return choices


def resolve_choice(choice: str, board: dict, character: dict, should_exit: bool, rested: bool) -> tuple[bool, bool]:
    """
    Execute the chosen action.

    :param choice: a string representing the player's choice
    :param board: a dictionary that represents the game board
    :param character: a dictionary representing the player
    :param should_exit: a boolean indicating if the game should exit or not
    :param rested: a boolean indicating if the player has rested or not
    :precondition: board must be a dictionary that follows the format of the game board,
                   with valid keys and values
    :precondition: character must be a dictionary that follows the format of a game character,
                   with valid keys and values
    :precondition: should_exit must be a boolean
    :rested: rested must be a boolean
    :postcondition: the player's action is executed and the relevant changes to the game state are made
    :return: a tuple containing two boolean values: `should_exit` and `rested`
    :raises: ValueError if `choice` is not a valid option
    """
    if choice in DIRECTIONS:
        should_exit = move_character(character, choice)
    elif choice in INTERACTIONS:
        if choice == "npc":
            enter_shop(board[character["location"]]["npc"], character)
        else:
            should_exit = initialize_boss_fight(character)
    elif choice == "inspect":
        inspect_self(character)
    elif choice == "rest":
        character["stats"]["current_hp"] = get_max_hp(character)
        slow_print("You catch your breath and feel refreshed")
        rested = True
    return should_exit, rested


def random_encounter(board: dict, character: dict):
    """
    Generate a random coordinate within the board that is not currently occupied by the player or a boss

    :param board: a dictionary that represents the game board, with keys as (x, y) tuples and values as characters
    :param character: a dictionary representing the player, with keys "name" and "location"
    :precondition: board must be a dictionary with at least one empty spot
    :postcondition: if a valid coordinate is found, returns a tuple of integers representing the (x, y)
    :postcondition: if the player is on the only remaining empty spot or a boss is nearby, return False
    :return: a tuple of integers representing the (x, y), or False if no valid coordinate is found
    """
    if has_boss(board, character["location"]):
        return False
    return check_for_foes()


def check_for_foes() -> bool:
    """
    Determine whether the player should encounter a foe after a move, with a 33% chance of encounter.

    Generates a random integer between 1 and 4, and returns True if the result is 2 for a 33% chance,
    indicating a foe encounter, and False otherwise.

    :postcondition: returns True if the player should encounter a foe, and False otherwise
    :return: a boolean indicating whether a foe is encountered
    """
    return random.randint(1, 3) == 2


def resolve_location(board, character):
    """
    Resolve the player's action within the current location on the game board.

    :param board: a dictionary that represents the game board
    :param character: a dictionary representing the player
    :precondition: board must be a dictionary with valid keys and values
    :precondition: character must be a dictionary with valid keys and values
    :postcondition: the player's action is resolved within the current location on the game board
    :return: None
    """
    should_exit = False
    rested = False
    while not should_exit:
        options = determine_choices(board, character, rested)
        choice = get_user_choice(options, "What would you like to do?\n")
        should_exit, rested = resolve_choice(choice, board, character, should_exit, rested)


def teleport_player_to_boss(character, random_npc_location):
    """
    Teleport the player to the location of the boss NPC on the game board.

    :param character: a dictionary representing the player
    :param random_npc_location: a tuple representing the location of the boss NPC on the game board
    :precondition: character must be a dictionary with valid keys and values
    :precondition: random_npc_location must be a tuple with valid x and y coordinates on the game board
    :postcondition: the player is teleported to the location of the boss NPC on the game board
    :return: None
    >>> test_character = {"name": "Calico", "location": (0, 0)}
    >>> test_random_npc_location = (2, 2)
    >>> teleport_player_to_boss(test_character, test_random_npc_location)
    You feel the world warp around you...
    ...
    As your vision clears, you see a giant devilish cat in front of you
    """
    slow_print("You feel the world warp around you...")
    slow_print("...")
    slow_print("As your vision clears, you see a giant devilish cat in front of you")
    character["location"] = random_npc_location


def spawn_boss(board: dict, character: dict) -> bool:
    """
    Spawns a boss on the game board if the player's level is greater than 2.

    :param board: a dictionary that represents the game board
    :param character: a dictionary representing the player
    :precondition: board must be a dictionary containing the game board data in the specified format
    :precondition: character must be a dictionary containing the player's data in the specified format
    :postcondition: if the player's level is greater than 2, a boss is spawned at a random location on
                    the game board and the boss's name is changed to "boss"
    :postcondition: if the player is at the location of the boss when it spawns,
                    the boss appears on the same location as the NPC
    :postcondition: if the NPC is not at the player's location, the player is teleported to the location
                    of the boss
    :return: True if a boss was spawned, False otherwise
    """
    if character["stats"]["level"] > 2:
        slow_print("\n...\nYou sense that a great evil has descended on the world")
        random_npc_location = random.choice(board["npcs"])
        npc = board[random_npc_location]['npc']

        if character["location"] == random_npc_location:
            slow_print(f"You see a streak of red light strike {npc['name']}!")
            slow_print(f"When the smoke clears, you see a giant devilish cat on a pool of blood where"
                       f" {npc['name']} was just standing")
        else:
            slow_print(f"You see a streak of red light strike somewhere far away")
            slow_print(f"You sense that {npc['name']} has died.")
            teleport_player_to_boss(character, random_npc_location)
        npc['name'] = "boss"
        return True
    return False


def resolve_monsters(character: dict, monsters: dict, gold: int):
    """
    Resolve a combat encounter between the player character and a group of monsters.

    :param character: a dictionary representing the player character
    :param monsters: a dictionary representing the monsters the player will fight
    :param gold: a positive integer representing the amount of gold the player will receive if they win the fight
    :precondition: character must be a dictionary with keys "stats" and "inventory"
    :precondition: character's "stats" key must contain keys "health" and "attack"
    :precondition: character's "inventory" key must contain a key "weapons" that is a dictionary
                   with keys "name" and "damage"
    :precondition: monsters must be a dictionary with keys "name", "health", and "attack"
    :postcondition: the combat encounter will be resolved, either with the player winning and receiving gold,
                    or the player losing and restarting the game
    """
    options = [("fight", f" 1: Attack"), ("run", f" 2: Run")]
    choice = get_user_choice(options, "What would you like to do?\n")
    if choice == "fight":
        initialize_combat(character, monsters, gold)
    else:
        flee_combat(character, monsters)


def save_game(character: dict, board: dict) -> None:
    """
    Save the game by writing the character and board data to files.

    :param character: a dictionary representing the player
    :param board: a dictionary representing the game board
    :precondition: character must be a dictionary
    :precondition: board must be a dictionary
    :postcondition: character data is saved as "character.txt" in the same directory
    :postcondition: board data is saved as "board.txt" in the same directory
    :return: None
    """
    save_to_file("character.txt", character)
    formatted_board = [{'key': key, 'value': value} for key, value in board.items()]
    save_to_file("board.txt", formatted_board)


def load_game() -> tuple[dict, dict]:
    """
    Load the game by reading the character data from "character.txt" and board data from "board.txt".

    :precondition: "character.txt" and "board.txt" must exist in the same directory
    :postcondition: if the files exist, character and board are loaded from the files,
                    formatted and returned as a tuple
    :postcondition: if the files don't exist, return None, None
    :return: a tuple containing character and board dictionaries, respectively
    """
    try:
        character = read_from_file("character.txt")
        formatted_board = read_from_file("board.txt")
        slow_print("A saved game was detected. Would you like to load it?")
        options = [("new", f" 1: New Game"), ("load", f" 2: Load Game")]
        choice = get_user_choice(options, "What would you like to do?\n")
        if choice == "new":
            return None, None
    except FileNotFoundError:
        return None, None
    character["location"] = tuple(character["location"])
    board = {}
    for item in formatted_board:
        key = tuple(item["key"]) if isinstance(item["key"], list) else item["key"]
        board[key] = item["value"]
    board["npcs"] = [tuple(item) for item in board["npcs"]]
    return character, board


def intro_story():
    """
    Print the introductory story for the game and display an ASCII art.

    :postcondition: prints the intro story as a string
    :return: None
    """
    slow_print("As you walk through the town, you hear a commotion near the town square.\n"
               "Following the meowing, you find a mysterious cat.\n"
               "But a shadowy figure snatches it away. You must embark on a perilous journey\n"
               "to save the cat, battling fierce foes and overcoming treacherous obstacles.\n"
               "Are you up for the challenge?")
    sleep(0.7)
    print("""                                                                          
     _____                 ___            _      _____                 _   
    |  _  | _ _  ___  ___ |  _| ___  ___ | |_   |     | _ _  ___  ___ | |_ 
    |   __|| | ||  _||  _||  _|| -_||  _||  _|  |  |  || | || -_||_ -||  _|
    |__|   |___||_|  |_|  |_|  |___||___||_|    |__  _||___||___||___||_|  
                                                   |__|                    
    """)
    sleep(0.7)


def game_ending():
    """
    Print the game ending and display an ASCII art.

    :postcondition: prints the game ending story as a string
    :return: None
    """
    slow_print("\nAfter the successful rescue, the cat suddenly transforms into a wizened old wizard,\n"
               "revealing that it was a shape-shifting feline all along. The wizard thanks you\n"
               "for your bravery and offers you a reward for your help.\n\n"
               "You expect something grand and powerful, but instead, the wizard offers you\n"
               "something that will make your feline friends happy: a lifelong supply\n"
               "of the finest catnip. As a magical ingredient with an addictive aroma,\n"
               "you know that it is the perfect reward for any cat lover.\n\n"
               "You thank the wizard for his generous gift, feeling satisfied that you were able\n"
               "receive a reward that will bring joy to you and your furry friends for years to come!")
    sleep(0.7)
    print("""
                                                  
             _____                        _____         _ 
            |  |  | ___  ___  ___  _ _   |   __| ___  _| |
            |     || .'|| . || . || | |  |   __||   || . |
            |__|__||__,||  _||  _||_  |  |_____||_|_||___|
                        |_|  |_|  |___|                   
            

         
              ,/|         _.--''^``-...___.._.
             /,  '\     _-'          ,--,,,--'
            { \    `_-''           /}
             `;;'            ;   ; ;
           .--''     ._,,, _..'  .;.'
          (,_....----'''     (,..--''
           """)


def game_over():
    """
    Print the game over message.

    :postcondition: prints the game over message as a string
    :return: None
    """
    slow_print("\nLooks like your cat-saving skills need a little purr-fecting.\n"
               "Game over, but don't let it whisker your spirits!\n"
               "Perhaps next time, you'll be able to claw your way to victory.")


def game():
    """
    Initialize the game.
    """
    rows = 5
    columns = 5
    character, board = load_game()
    if not character and not board:
        board = make_board(rows, columns)
        character = make_character()
        intro_story()
    while not character["flags"]["achieved_goal"]:
        save_game(character, board)
        has_monsters = random_encounter(board, character)
        describe_current_location(board, character)
        if has_monsters:
            monsters, gold = generate_monsters(character)
            slow_print(describe_monsters(monsters))
            resolve_monsters(character, monsters, gold)
        if still_alive(character):
            resolve_location(board, character)
            if not character["flags"]["boss_spawned"]:
                character["flags"]["boss_spawned"] = spawn_boss(board, character)
        else:
            break
    if not character["flags"]["achieved_goal"]:
        game_over()
    else:
        game_ending()


def main() -> None:
    """
    Drive the program.
    """
    game()


if __name__ == "__main__":
    main()
