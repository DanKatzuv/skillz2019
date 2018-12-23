from elf_kingdom import *

# Constants
center = Location(1800, 3500)
BUILD_THRESH = 100
portals_upper = [Location(1200, 4600), Location(800, 3400)]
portals_lower = [Location(2500, 1500), Location(3000, 3200)]

# Globals
upper = False
builds = {}


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


def handle_elves(game):
    portals = portals_upper if upper else portals_lower
    try:
        build_portal(game.get_my_living_elves()[0], portals[0])
        build_portal(game.get_my_living_elves()[1], portals[1])
    except Exception as e:
        print(e)


def build_portal(elf, loc):
    """Build a Portal."""
    global builds
    print("Moving to {}".format(loc))
    elf.move_to(loc)
    if elf not in builds:
        builds[elf] = loc


def handle_builds():
    global builds, BUILD_THRESH
    for elf, loc in builds.items():
        if elf.get_location().distance(loc) < BUILD_THRESH:
            print("Building portal")
            elf.build_portal()
            builds.pop(elf)
        else:
            elf.move_to(loc)
