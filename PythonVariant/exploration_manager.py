"""
Manage exploration aspect of challenge
"""

import threading as t
import time
import ship_commands as sc
import game_constants as const


class ExplorationManager(t.Thread):
    """
    Class to manage exploration thread
    """

    def __init__(self, conn, state):
        self.conn = conn
        self.state = state
        super().__init__()

    def run(self):
        """
        Begin exploring
        """
        print("Beginning to explore...")
        ship_paths = {}
        planned_dests = {}
        ships_visited = {}

        while True:
            systems = self.state.get_systems()
            ships = self.state.get_ships()
            # Do we actually have a state yet?
            if not ships:
                time.sleep(0.1)
                continue
            remove_arrived_destinations(ships, planned_dests)
            self.do_observations(ships, systems)
            # Done yet?
            accessable = get_accessable_systems(ships, systems)
            if len(systems) == len(accessable):
                print("Finished Exploring!")
                return
            # We haven't gone everywhere yet
            self.move_ships(ships, ship_paths, systems,
                            ships_visited, planned_dests)

    def do_observations(self, ships, systems):
        """
        Observe any systems that ships are in if they
        have not been observed already
        """
        observed = get_system_list(systems)
        for ship in ships:
            if ship[const.STATUS] != const.AWAITING:
                continue
            if ship[const.LOCATION] not in observed:
                sys = sc.observe(self.conn, ship)
                systems.append(sys)
                observed.append(sys[const.NAME])
                self.state.add_update_system(sys)

    def move_ships(
            self, ships, ship_paths, systems, ships_visited, planned_dests):
        """
        Move the ships around to explore
        """
        for ship in ships:
            if ship[const.STATUS] != const.AWAITING:
                continue
            curr_system = get_system_by_name(ship[const.LOCATION], systems)
            # Go unexplored or go back
            if not ship[const.NAME] in ship_paths:
                ship_paths[ship[const.NAME]] = []
            add_ships_visited(ships, ships_visited)
            dest = get_destination(
                ship[const.NAME], curr_system, ship_paths[ship[const.NAME]],
                ships_visited, planned_dests)
            if dest:
                planned_dests[ship[const.NAME]] = dest
                sc.move(self.conn, ship, dest)
                self.state.add_update_ship(ship)


def get_destination(
        ship_name, system, ship_path, ships_visited, planned_dests):
    """
    Get the optimal destination for the ship based on the provided data
    """
    dest = None
    dest_rating = {}
    visited = [item for sublist in ships_visited.values() for item in sublist]
    for lane in system[const.HYPERLANES]:
        if lane not in ships_visited[ship_name]:
            rating = 1
            if lane not in visited:
                rating = 2
                if lane not in planned_dests.values():
                    rating = 3
            dest_rating[lane] = rating
        if dest_rating:
            best_rating = max(dest_rating.values())
            for rated_dest in dest_rating.keys():
                if dest_rating[rated_dest] == best_rating:
                    dest = rated_dest
                    break
    if dest is None:
        if ship_path:
            dest = ship_path.pop()
    else:
        ship_path.append(system[const.NAME])
    return dest


def get_accessable_systems(ships, systems):
    """
    Determine which systems are currently accessable
    """
    accessable = []
    for ship in ships:
        if ship[const.LOCATION] not in accessable:
            accessable.append(ship[const.LOCATION])
    for system in systems:
        if system[const.NAME] not in accessable:
            accessable.append(system[const.NAME])
        for lane in system[const.HYPERLANES]:
            if lane not in accessable:
                accessable.append(lane)
    return accessable


def get_system_list(systems):
    """
    Get the list of system names
    """
    sys_list = []
    for system in systems:
        if system[const.NAME] not in sys_list:
            sys_list.append(system[const.NAME])
    return sys_list


def get_system_by_name(name, systems):
    """
    Find the system in a list based on it's name
    """
    for system in systems:
        if name == system[const.NAME]:
            return system
    return None


def remove_arrived_destinations(ships, planned_dests):
    """
    Remove any destinations we've arrived at from the planned destinations
    """
    for ship in ships:
        if ship[const.NAME] in planned_dests:
            if planned_dests[ship[const.NAME]] == ship[const.LOCATION]:
                del planned_dests[ship[const.NAME]]


def add_ships_visited(ships, ships_visted):
    """
    Add any current locations to the list of places visited
    """
    for ship in ships:
        if ship[const.NAME] not in ships_visted:
            ships_visted[ship[const.NAME]] = []
        if ship[const.LOCATION] not in ships_visted[ship[const.NAME]]:
            ships_visted[ship[const.NAME]].append(ship[const.LOCATION])
