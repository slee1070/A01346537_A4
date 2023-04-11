"""
Sung Lee
A01346537
"""

from time import sleep
import json


def slow_print(line: str, speed: float = 0.02):
    """
    Print a string character-by-character at a given speed.

    :param line: a string to be printed
    :param speed: a float representing the time delay between printing each character
    :precondition: line must be a string
    :precondition: speed must be a float
    :postcondition: the string is printed character-by-character at the given speed
    :return: None
    >>> slow_print("hello")
    hello
    """
    for character in line:
        print(character, end="", flush=True)
        sleep(speed)
    print()


def get_user_choice(choices: list, prompt: str) -> str:
    """
    Displays a list of options and prompts the user to choose one.

    :param choices: a list of tuples representing the available options, where each tuple contains
                    a string representing the option's label and a string representing the option's description
    :param prompt: a string representing the prompt to display to the user
    :precondition: choices must be a non-empty list of tuples
    :precondition: prompt must be a non-empty string
    :postcondition: displays the available options and prompts the user to choose one
    :return: a string representing the chosen option
    :raises ValueError: if the user's input is not a valid choice
    :raises TypeError: if the input parameters are of the wrong type
    :raises IndexError: if the list of choices is empty
    """
    while True:
        slow_print(prompt)
        for option in choices:
            slow_print(f"{option[1]}", 0.0)
        try:
            slow_print("\nEnter a number to make your choice:")
            choice = int(input())
            if choice > len(choices) or choice < 1:
                raise ValueError("Invalid input")
            return choices[choice - 1][0]
        except ValueError:
            slow_print("Sorry, you can't do that.")


def save_to_file(filename: str, dictionary: dict):
    """
    Save a dictionary to a file in JSON format.

    :param filename: a string representing the name of the file to save
    :param dictionary: a dictionary representing the data to save
    :precondition: filename must be a valid file name as a string
    :precondition: dictionary must be a dictionary
    :postcondition: dictionary is saved to the specified file in JSON format
    :return: None
    """
    data = json.dumps(dictionary)
    with open(filename, 'w') as output:
        output.write(data)


def read_from_file(filename: str) -> dict:
    """
    Read a dictionary object from a JSON file.

    :param filename: a string representing the filename of the JSON file to be read
    :precondition: the file must exist and be a valid JSON file
    :postcondition: the contents of the JSON file will be loaded into a dictionary object
    :return: a dictionary object containing the contents of the JSON file
    :raises: FileNotFoundError if the specified file does not exist or is not readable
    :raises: JSONDecodeError if the specified file is not a valid JSON file
    """
    with open(filename) as file_object:
        contents = file_object.read()
        data = json.loads(contents)
        return data
