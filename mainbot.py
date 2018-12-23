from elf_kingdom import *

# Constants
center = Location(1800, 3500)
BUILD_THRESH = 100

# Globals
upper = False
builds = {}
attack_elves = []
defense_elves = []
built = False
building_defense = False


def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    global upper
    upper = game.get_my_castle().get_location().row > game.get_enemy_castle().get_location().row
    handle_elves(game)
    handle_builds()
    send_giants_to_enemy_castle(game)
    send_trolls_to_our_castle(game)


def handle_elves(game):
    build_defense_portal(game.get_my_living_elves()[0], game)
    build_attack_portals(attack_elves, game)


def build_defense_portal(elf, game):
    """Build a Portal near the enemy Castle."""
    global building_defense
    if not building_defense:
        global builds, upper
        modifier = -1000
        if not upper:
            modifier = 1000
        loc = Location(game.get_my_castle().get_location().row + modifier,
                       game.get_my_castle().get_location().col - modifier)
        print("Moving to {}".format(loc))
        elf.move_to(loc)
        builds[elf] = loc
        building_defense = True


def handle_builds():
    global builds, BUILD_THRESH
    for elf, loc in builds.items():
        if elf.get_location().distance(loc) < BUILD_THRESH:
            print("Building portal")
            elf.build_portal()
            builds.pop(elf)
        else:
            elf.move_to(loc)


def build_attack_portals(elves, game):
    pass


def send_giants_to_enemy_castle(game):
    if not built:
        return
    try:
        attack_portal = game.get_my_portals()[1]
        attack_portal.summon_lava_giant()

    except Exception as e:
        print(e)
        pass


def send_trolls_to_our_castle(game):
    if not built:
        return
    if not built and game.get_my_mana() > 60:
        defense_portal = game.get_my_portals()[0]
        defense_portal.summon_ice_troll()
        return
    try:
        defense_portal = game.get_my_portals()[0]
        defense_portal.summon_ice_troll()
    except Exception as e:
        print(e)
        pass


def handle_portals(game):
    pass
