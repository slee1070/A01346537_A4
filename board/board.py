"""
Sung Lee
A01346537
"""

import random

from board import SHOP_INVENTORY, ADJECTIVES, PLACES
from helper import VOWELS


def get_random_coordinate(board: dict) -> tuple:
    x = random.randint(0, board["dimensions"]["rows"] - 1)
    y = random.randint(0, board["dimensions"]["columns"] - 1)
    return x, y


def place_npcs(board: dict) -> None:
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
    coordinate = random.choice(board["npcs"])
    board[coordinate]["npc"] = {
        "name": "boss"
    }


def has_npc(board: dict, coordinate: tuple) -> bool:
    return coordinate in board["npcs"]


def has_boss(board: dict, coordinate: tuple) -> bool:
    return board[coordinate]["npc"] and board[coordinate]["npc"]["name"] == "boss"


def make_board(rows: int, columns: int) -> dict:
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
