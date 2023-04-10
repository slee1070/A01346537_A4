"""
Sung Lee
A01346537
"""

import itertools
import random

from board.board import has_npc, has_boss, make_board
from board.shop import enter_shop
from character.character import move_character, inspect_self, make_character, still_alive, get_max_hp
from character.monster import generate_monsters
from combat.combat import initialize_combat, initialize_boss_fight, describe_monsters, flee_combat
from helper import INTERACTIONS, DIRECTIONS
from helper.print_helper import slow_print, get_user_choice


def describe_current_location(board: dict, character: dict) -> None:
    current_coordinates = character["location"]
    current_location = board[current_coordinates]
    slow_print(f"\nYou are currently in {current_location['description']} {current_coordinates}")


def get_valid_directions(board: dict, character: dict) -> list:
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
    character_coordinate = character["location"]
    directions = get_valid_directions(board, character)
    choices = [(pair[1], f" {pair[0]}: Go {pair[1]}") for pair in zip(itertools.count(1), directions)]
    npc_present = character_coordinate in board["npcs"]
    if npc_present:
        if has_boss(board, character_coordinate):
            choices.append(("boss", f" {len(choices) + 1}: Start final fight with the big bad evil cat"))
        else:
            choices.append(("npc", f" {len(choices) + 1}: Talk to {board[character_coordinate]['npc']['name']}"))
    choices.append(("inspect", f" {len(choices) + 1}: Inspect yourself"))
    if not rested:
        choices.append(("rest", f" {len(choices) + 1}: Rest and recover your health"))
    return choices


def resolve_choice(choice: str, board: dict, character: dict, should_exit: bool, rested: bool) -> tuple[bool, bool]:
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


def intro_story():
    pass


def resolve_location(board, character):
    should_exit = False
    rested = False
    while not should_exit:
        options = determine_choices(board, character, rested)
        choice = get_user_choice(options, "What would you like to do?\n")
        should_exit, rested = resolve_choice(choice, board, character, should_exit, rested)


def teleport_player_to_boss(character, random_npc_location):
    slow_print("You feel the world warp around you...")
    slow_print("...")
    slow_print("As your vision clears, you see a giant devilish cat in front of you")
    character["location"] = random_npc_location


def spawn_boss(board: dict, character: dict) -> bool:
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
    options = [("fight", f" 1: Attack"), ("run", f" 2: Run")]
    choice = get_user_choice(options, "What would you like to do?\n")
    if choice == "fight":
        initialize_combat(character, monsters, gold)
    else:
        flee_combat(character, monsters)


def game():
    """
    Initialize the game.
    """
    rows = 5
    columns = 5
    boss_spawned = False
    board = make_board(rows, columns)
    character = make_character()
    intro_story()
    while not character["flags"]["achieved_goal"]:
        has_monsters = random_encounter(board, character)
        describe_current_location(board, character)
        if has_monsters:
            monsters, gold = generate_monsters(character)
            slow_print(describe_monsters(monsters))
            resolve_monsters(character, monsters, gold)
        resolve_location(board, character)
        if still_alive(character):
            if not boss_spawned:
                boss_spawned = spawn_boss(board, character)
        else:
            break
    if not character["flags"]["achieved_goal"]:
        slow_print("You lose")
    else:
        slow_print("You won")


def main() -> None:
    """
    Drive the program.
    """
    game()


if __name__ == "__main__":
    main()
