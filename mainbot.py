from elf_kingdom import *
# Game constants
CENTER = Location(1800, 3500) #default

setup_boolean = False
# Constants
BUILD_THRESH = 100
DEFENSE_PORTAL_DISTANCE = 2000
portals_lower = [Location(1200, 4600), Location(1800, 3500)]
portals_upper = [Location(2500, 1500), Location(1800, 3500)]

# Globals
upper = False
builds = {}


def setup(game):
    global CENTER
    CENTER = location_average(game.get_enemy_castle(), game.get_my_castle())
        return
    for portal in game.get_my_portals():
        print portal.get_location()
        if portal.get_location().distance(center) <= BUILD_THRESH:
            print "Equals"
            return
    nearest_elf = min(game.get_my_living_elves(), key=lambda elf: elf.distance(center))
    build_portal(nearest_elf, center)


def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    global setup_boolean
    global upper

    if not setup_boolean:
        setup(game)
        setup_boolean = True

    upper = game.get_my_castle().get_location().row > game.get_enemy_castle().get_location().row
    handle_elves(game)
    handle_builds()
    portal_handling(game)
    elf_attack_nearest_target(game)
    fix_center_portal(game)


def nearest_target_for_elf(game, game_object):
    targets = game.get_enemy_portals() + game.get_enemy_living_elves()
    try:
        return min(targets, key=lambda target: game_object.distance(target))
    except ValueError:
        return


def is_portal_endangered(game, portal):
    """Return whether an enemy Elf is endangering a Portal."""
    return any(portal.distance(enemy_elf.location) < game.elf_attack_range
               for enemy_elf in game.get_enemy_living_elves())


def portal_handling(game):
    if builds and game.get_my_mana() < 120:
        return

    defense_portals = [portal for portal in game.get_my_portals() if
                       game.get_my_castle().distance(portal) < DEFENSE_PORTAL_DISTANCE]
    attack_portals = [portal for portal in game.get_my_portals() if portal not in defense_portals]

    for portal in game.get_my_portals():
        if is_portal_endangered(game, portal):
            portal.summon_ice_troll()

    for defense_portal in defense_portals:
        if defense_portal.can_summon_ice_troll():
            defense_portal.summon_ice_troll()
    for attack_portal in attack_portals:
        if attack_portal.can_summon_lava_giant():
            attack_portal.summon_lava_giant()


def elf_attack_nearest_target(game):
    for elf in game.get_my_living_elves():
        print("cond: {}".format(elf not in builds and not elf.is_building))
        attack_object(game, elf, nearest_target_for_elf(game, elf))  # tells the elf to attack the nearest target


def handle_elves(game):
    if not game.get_my_living_elves():
        return
    portals = portals_upper if upper else portals_lower
    if len(game.get_my_portals()) > 1 and len(game.get_my_living_elves()) == 2:
        return
    try:
        build_portal(game.get_my_living_elves()[0], portals[0])
        if len(game.get_my_portals()) <= 2:
            build_portal(game.get_my_living_elves()[1], portals[1])
    except Exception as e:
        print(e)


def handle_builds():
    global builds, BUILD_THRESH
    for elf, loc in builds.items():
        print elf
        if elf is None:
            continue
        try:
            if elf.get_location().distance(loc) < BUILD_THRESH:
                print("Building portal")
                elf.build_portal()
                builds.pop(elf)
            else:
                elf.move_to(loc)
        except AttributeError:
            continue


### METHODS ###
def build_portal(elf, loc):
    """Build a Portal."""
    global builds
    print("Moving to {}".format(loc))
    if elf not in builds:
        builds[elf] = loc


def attack_object(game, elf, obj):

    if not obj or not elf.is_alive() or elf in builds or elf.is_building:
        return
    if elf.get_location().distance(obj) < game.elf_attack_range:
        elf.attack(obj)
    else:
        elf.move_to(obj)


### UTILITIES ###
def location_average(l1, l2):
    if not isinstance(l1, Location):
        l1 = l1.get_location()
    if not isinstance(l2, Location):
        l2 = l2.get_location()
    return Location((l1.row + l2.row) / 2, (l1.col + l2.col) / 2)
