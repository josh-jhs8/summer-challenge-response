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
		ship_path = {}

		while True:
			systems = self.state.get_systems()
			ships = self.state.get_ships()
			#Do we actually have a state yet?
			if not ships:
				time.sleep(0.1)
				continue
			self.do_observations(ships, systems)
			#Done yet?
			accessable = get_accessable_systems(ships, systems)
			if len(systems) == len(accessable):
				print("Finished Exploring!")
				return
			#We haven't gone everywhere yet
			self.move_ships(ships, ship_path, systems)


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

	def move_ships(self, ships, ship_path, systems):
		"""
		Move the ships around to explore
		"""
		for ship in ships:
			if ship[const.STATUS] != const.AWAITING:
				continue
			observed = get_system_list(systems)
			curr_system = get_system_by_name(ship[const.LOCATION], systems)
			#Go unexplored or go back
			if not ship[const.NAME] in ship_path:
				ship_path[ship[const.NAME]] = []
			dest = get_destination(ship_path[ship[const.NAME]], curr_system, observed)
			if dest:
				sc.move(self.conn, ship, dest)
				self.state.add_update_ship(ship)

def get_destination(ship_path, system, observed):
	"""
	Get the optimal destination for the ship based on the provided data
	"""
	dest = None
	for lane in system[const.HYPERLANES]:
		if lane not in observed:
			dest = lane
	if dest is None:
		#if ship[const.NAME] in ship_path and ship_path[ship[const.NAME]]:
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
