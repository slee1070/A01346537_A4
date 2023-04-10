"""
Sung Lee
A01346537
"""

import random

from board import SHOP_INVENTORY, ADJECTIVES, PLACES
from helper import VOWELS


def get_random_coordinate(board: dict) -> tuple:
    """
    Generate a random coordinate within the board.

    :param board: a dictionary that represents the game board
    :precondition: board must have greater than 1 row and column
    :precondition: board must have a ["dimensions"]["rows"] value that reprents the number of rows
    :precondition: board must have a ["dimensions"]["columns"] value that reprents the number of columns
    :postcondition: a random coordinate is generated between 0 and max row and column
    :return: a coordinate as a tuple
    >>>
    """
    x = random.randint(0, board["dimensions"]["rows"] - 1)
    y = random.randint(0, board["dimensions"]["columns"] - 1)
    return x, y


def place_npcs(board: dict) -> None:
    """
    Add three NPCs to the board.

    :param board: a dictionary that represents the game board
    :precondition: board must have at least three cells
    :postcondition: Merchant, Monk Brando and Monk Sando are randomly added to unique cells on the board
    >>>
    """
    list_of_coordinates = set()
    while len(list_of_coordinates) < 3:
        list_of_coordinates.add(get_random_coordinate(board))

    list_of_coordinates = list(list_of_coordinates)
    board["npcs"] = list_of_coordinates
    board[list_of_coordinates[0]]["npc"] = {
        "name": "Merchant",
        "inventory": SHOP_INVENTORY
    }
    board[list_of_coordinates[1]]["npc"] = {
        "name": "Monk Brando"
    }
    board[list_of_coordinates[2]]["npc"] = {
        "name": "Monk Sando"
    }


def place_boss(board: dict) -> None:
    """
    Add the boss to the board.

    :param board: a dictionary that represents the game board
    :precondition: the board has a list of NPC coordinates
    :postcondition: the boss is randomly placed at one of the NPC coordinates
    >>>
    """
    coordinate = random.choice(board["npcs"])
    board[coordinate]["npc"] = {
        "name": "boss"
    }


def has_boss(board: dict, coordinate: tuple) -> bool:
    """
    Check if a coordinate on the board has the boss.

    :param board: a dictionary that represents the game board
    :param coordinate: a tuple of x and y coordinates
    :precondition: the board has at least 1 cell
    :precondition: coordinate is within the board
    :postcondition: True is returned if the coordinate has the boss, False otherwise
    :return: True if the coordinate has the boss, False otherwise
    :raises: KeyError: if the coordinate is not within the board
    >>>
    """
    try:
        return board[coordinate]["npc"] and board[coordinate]["npc"]["name"] == "boss"
    except KeyError:
        return False


def make_board(rows: int, columns: int) -> dict:
    """
    Generate the game board.

    :param rows: a positive integer to indicate the number of rows on the board
    :param columns: a positive integer to indicate the number of columns on the board
    :precondition: rows must be a positive integer greater than 0
    :precondition: columns must be a positive integer greater than 0
    :postcondition: a rows x columns grid is generated along with NPCs and a text description of each cell
    :return: a dictionary representing the game board
    >>>
    """
    def generate_location_description():
        adjective = random.choice(ADJECTIVES)
        place = random.choice(PLACES)
        if adjective[0] in VOWELS:
            description_text = "an "
        else:
            description_text = "a "
        description_text += f"{adjective} {place}"
        return description_text

    board = {"npcs": []}
    for row in range(rows):
        for column in range(columns):
            coordinates = (row, column)
            description = generate_location_description()
            board[coordinates] = {
                "description": description,
                "npc": {}
            }
            board["dimensions"] = {
                "rows": rows,
                "columns": columns
            }
    place_npcs(board)
    return board
