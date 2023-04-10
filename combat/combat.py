import random

from character.character import still_alive, check_for_level_up, get_attack_strength
from character.monster import generate_boss
from helper import VOWELS
from helper.print_helper import slow_print, get_user_choice


def describe_monsters(monsters):
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


def calculate_damage(attacker):
    damage = get_attack_strength(attacker)
    dice_result = random.randint(1, 20)
    slow_print(f"...and rolled {dice_result}!")

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


def player_attacks(character, monsters):
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


def monsters_attack(character, monsters):
    for monster in monsters:
        slow_print(f"The {monster['monster']} attacks...")
        slow_print(f"The {monster['monster']} roll a d20")
        damage = calculate_damage(monster)

        slow_print(f"It deals {damage} damage to you.")
        character["stats"]["current_hp"] -= damage
        if not still_alive(character):
            print("You died!")
            return


def determine_sneak(character, monsters) -> bool:
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


def gain_rewards(character: dict, gold: int):
    slow_print("\nYou are victorious!")
    slow_print(f"You found {gold} gold.")
    character["gold"] += gold
    character["stats"]["victories"] += 1
    check_for_level_up(character)


def enter_combat(character: dict, monsters: list):
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


def continue_attack():
    attack = True
    options = [("fight", f" 1: Attack"), ("run", f" 2: Run")]
    choice = get_user_choice(options, "What would you like to do?\n")
    if choice == "run":
        attack = False
    return attack


def flee_combat(character: dict, monsters: list):
    monster = random.choice(monsters)
    damage = monster["stats"]["attack"]
    slow_print(f"You successfully fled but the {monster['monster']} hits you for {damage} damage")
    character["stats"]["current_hp"] -= damage


def initialize_combat(character: dict, monsters, gold):
    victorious = enter_combat(character, monsters)
    if victorious and still_alive(character):
        gain_rewards(character, gold)


def initialize_boss_fight(character: dict):
    monsters, gold = generate_boss(character)
    victorious = enter_combat(character, monsters)
    if victorious and still_alive(character):
        gain_rewards(character, gold)
        slow_print("You've done it! You've defeated the evil cat!")
        character["flags"]["achieved_goal"] = True
    return True
