import ship_commands as sc
import threading as t
import time
import game_constants as const

class ExplorationManager(t.Thread):
	def __init__(self, conn, state):
		self.conn = conn
		self.state = state
		super().__init__()

	def run(self):
		print("Beginning to explore...")
		ship_path = {}

		while True:
			systems = self.state.get_systems()
			ships = self.state.get_ships()
			#Do we actually have a state yet?
			if len(ships) < 1:
				time.sleep(0.1)
				continue
			#Have we observerd all the systems we're in
			observed = get_system_list(systems)
			for ship in ships:
				if ship[const.STATUS] != const.AWAITING:
					continue
				if ship[const.LOCATION] not in observed:
					s = sc.observe(self.conn, ship)
					systems.append(s)
					observed.append(s[const.NAME])
					self.state.add_update_system(s)
			#Done yet?
			accessable = get_accessable_systems(ships, systems)
			if len(systems) == len(accessable):
				print("Finished Exploring!")
				return
			#We haven't gone everywhere yet
			for ship in ships:
				if ship[const.STATUS] != const.AWAITING:
					continue
				curr_system = get_system_by_name(ship[const.LOCATION], systems)
				#Go unexplored or go back
				dest = None
				for lane in curr_system[const.HYPERLANES]:
					if lane not in observed:
						dest = lane
						break
				if dest == None:
					if ship[const.NAME] in ship_path and len(ship_path[ship[const.NAME]]) > 0:
						dest = ship_path[ship[const.NAME]].pop()
					else:
						continue
				else:
					if ship[const.NAME] not in ship_path:
						ship_path[ship[const.NAME]] = []
					ship_path[ship[const.NAME]].append(curr_system[const.NAME])
				sc.move(self.conn, ship, dest)
				self.state.add_update_ship(ship)



def get_accessable_systems(ships = [], systems = []):
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
	l = []
	for system in systems:
		if system[const.NAME] not in l:
			l.append(system[const.NAME])
	return l

def get_system_by_name(name, systems):
	for system in systems:
		if name == system[const.NAME]:
			return system
	return None