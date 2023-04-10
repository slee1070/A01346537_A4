"""
Sung Lee
A01346537
"""

from helper.print_helper import slow_print, get_user_choice


def checkout(choice: str, npc: dict, character: dict) -> None:
    """
    Purchase selected item.

    :param choice: a string representing the item to buy
    :param npc: a dictionary representing the merchant
    :param character: a dictionary representing the player
    :precondition: choice must be a string and exist in the NPC's inventory
    :precondition: NPC must be a dictionary that has an inventory dictionary
    :precondition: character must be a dictionary that has a gold key and integer value
    :postcondition: If character has gold equal to or greater than the item's cost, then the item is removed from the
                    merchant's inventory and added to the character's equipment
    >>>
    """
    item = npc["inventory"][choice]
    item_cost = item["cost"]
    wallet = character["gold"]
    if wallet >= item_cost:
        character["gold"] -= item_cost
        npc["inventory"].pop(choice)
        character["equipment"][choice] = item
        slow_print(f"You wear {choice} and suddenly you feel stronger!")
    else:
        slow_print(f"You look at the {choice} longingly but you can't afford it.")


def resolve_shopkeeper(npc: dict, character: dict) -> None:
    """
    Greet the player and show items the player can buy.

    :param npc: a dictionary representing the merchant
    :param character: a dictionary representing the player
    :precondition: npc must be a dictionary that has an inventory of items
    :precondition: character must be a dictionary that has a gold key and integer value
    :postcondition: the character is greeted and items are shown to the player
    >>>
    """
    slow_print("You enter the shop...")
    if len(npc["inventory"]) > 0:
        slow_print("Hello traveller, I have wares if you have coin.")
        slow_print(f"You check your wallet. You see {character['gold']} gold pieces.")
        options = [(item[0], f" {number}: {item[0]} | cost: {item[1]['cost']} gold | Boosts {item[1]['bonus']['stat']}"
                   f" by {item[1]['bonus']['amount']}") for number, item in enumerate(npc["inventory"].items(), 1)]
        options.append(("exit", f" {len(npc['inventory']) + 1}: Leave the shop."))

        choice = get_user_choice(options, "Select item to buy:\n")
        if choice in npc["inventory"]:
            checkout(choice, npc, character)
        else:
            slow_print("Thank you, please come again!")
    else:
        slow_print("Sorry, I have no more items to sell.")
    slow_print("You leave the shop...")


def resolve_atk_booster(character: dict) -> None:
    """
    Handle talking to the attack booster NPC.

    :param character: a dictionary representing the player
    :precondition: character must be a dictionary that has a flags dictionary
    :precondition: character must be a dictionary that has a stats dictionary
    :postcondition: if the character's atk_boosted flag is False, the character's attack stat is increased
    :postcondition: no boost takes place if the character's atk_boosted flag is True
    :postcondition: if atk_boosted is False, it is set to True
    >>>
    """
    slow_print(f"Hello {character['name']}. ")
    if not character["flags"]["atk_boosted"]:
        slow_print("I will now make you stronger!")
        character["flags"]["atk_boosted"] = True
        character["stats"]["attack"] += 7
        slow_print("You feel strength coursing through your body...")
    else:
        slow_print("There is nothing else I can do for you.")


def resolve_hp_booster(character: dict) -> None:
    """
    Handle talking to the attack booster NPC.

    :param character: a dictionary representing the player
    :precondition: character must be a dictionary that has a flags dictionary
    :precondition: character must be a dictionary that has a stats dictionary
    :postcondition: if the character's hp_boosted flag is False, the character's attack stat is increased
    :postcondition: no boost takes place if the character's hp_boosted flag is True
    :postcondition: if hp_boosted is False, it is set to True
    >>>
    """
    slow_print(f"Hello {character['name']}. ")
    if not character["flags"]["hp_boosted"]:
        slow_print("I will now make you stronger!")
        character["flags"]["hp_boosted"] = True
        character["stats"]["max_hp"] += 20
        character["stats"]["current_hp"] = character["stats"]["max_hp"]
        slow_print("You feel much healthier...")
    else:
        slow_print("There is nothing else I can do for you.")


def enter_shop(npc: dict, character: dict):
    """
    Determine how to interact with an NPC.

    :param npc: a dictionary representing an NPC
    :param character: a dictionary representing the player
    :precondition: npc has the key named
    :postcondition: the correct function is called
    >>>
    """
    if npc["name"] == "Merchant":
        resolve_shopkeeper(npc, character)
    elif npc["name"] == "Monk Brando":
        resolve_atk_booster(character)
    else:
        resolve_hp_booster(character)
