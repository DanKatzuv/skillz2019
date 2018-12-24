from elf_kingdom import *

# Constants
CASTLE_DEFENCE_DISTANCE = 2150
center = Location(1800, 3500)
BUILD_THRESH = 100
DEFENSE_PORTAL_DISTANCE = 2000  # radius from the castle, in it all portals are defined as defence portals.
portals_lower = [Location(1200, 4600), center]
portals_upper = [Location(2500, 1500), center]

# Globals
upper = False
builds = {}


def fix_center_portal(game):
    print game.get_my_living_elves()
    if not game.get_my_living_elves():
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
    global upper
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
    return is_group_near_object(portal, game.get_enemy_living_elves(), (game.elf_attack_range + game.portal_size / 2) * 2)


def is_group_near_object(friendly_object, enemy_list, distance):
    """Return whether any of the list of enemies are near a friendly object."""
    correct_group = [friendly_object.distance(enemy.location) < distance for enemy in enemy_list]
    return any(correct_group)  # , correct_group


def portal_handling(game):
    if builds and game.get_my_mana() < 120:
        return

    defense_portals = [portal for portal in game.get_my_portals() if
                       game.get_my_castle().distance(portal) < DEFENSE_PORTAL_DISTANCE]
    attack_portals = [portal for portal in game.get_my_portals() if portal not in defense_portals]

    for portal in game.get_my_portals():
        if is_portal_endangered(game, portal):
            portal.summon_ice_troll()

    if(is_group_near_object(game.get_my_castle(), game.get_enemy_living_elves() + game.get_enemy_lava_giants(), CASTLE_DEFENCE_DISTANCE)):
        for defense_portal in defense_portals:
            if defense_portal.can_summon_ice_troll():
                defense_portal.summon_ice_troll()
    for attack_portal in attack_portals:
        if attack_portal.can_summon_lava_giant():
            attack_portal.summon_lava_giant()


def elf_attack_nearest_target(game):
    for elf in game.get_my_living_elves():
        print("cond: {}".format(elf not in builds and not elf.is_building))
        if elf not in builds and not elf.is_building:
            target = nearest_target_for_elf(game, elf)
            if not target:
                return
            if elf.get_location().distance(target) < game.elf_attack_range:
                elf.attack(target)
            else:
                elf.move_to(target)


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


def build_portal(elf, loc):
    """Build a Portal."""
    global builds
    print("Moving to {}".format(loc))
    if elf not in builds:
        builds[elf] = loc


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


