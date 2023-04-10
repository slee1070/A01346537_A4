"""
Sung Lee
A01346537
"""

from time import sleep


def slow_print(line: str, speed: float = 0.02):
    for character in line:
        print(character, end="", flush=True)
        # sleep(speed)
    print()


def get_user_choice(choices: list, prompt: str) -> str:
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
