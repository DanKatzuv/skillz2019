from elf_kingdom import *

# Globals
attack_elves = []
defense_elves = []
built = False


def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    handle_elves_types(game)
    build_defense_portals(game)
    send_giants_to_enemy_castle(game)
    send_trolls_to_our_castle(game)


def handle_elves_types(game):
    """Assignes each Elf a role."""
    living_elves = game.get_my_living_elves()
    global attack_elves, defense_elves
    attack_elves = living_elves[:(len(living_elves) / 2) + 1]
    defense_elves = living_elves[len(living_elves) / 2:]


def build_defense_portals(game):
    """Build a Portal near the enemy Castle."""
    global built
    building_elf = attack_elves[0]
    enemy_castle = game.get_enemy_castle()
    enemy_castle_loc = enemy_castle.get_location()
    portal_loc = Location(enemy_castle_loc.row, enemy_castle_loc.col + enemy_castle.size)
    if not built:
        if building_elf.get_location().distance(portal_loc) < (enemy_castle.size + 100):
            built = True
            print("Building portal")
            building_elf.build_portal()
            return  # Exit when a portal was built
        print("Moving to {}".format(portal_loc))
        building_elf.move_to(portal_loc)


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
