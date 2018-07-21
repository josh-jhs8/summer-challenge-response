import ship_commands as sc
import threading as t
import time

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
				if ship["Status"] != "Awaiting Command":
					continue
				if ship["Location"] not in observed:
					s = sc.observe(self.conn, ship)
					systems.append(s)
					observed.append(s["Name"])
					self.state.add_update_system(s)
			#Done yet?
			accessable = get_accessable_systems(ships, systems)
			if len(systems) == len(accessable):
				print("Finished Exploring!")
				return
			#We haven't gone everywhere yet
			for ship in ships:
				if ship["Status"] != "Awaiting Command":
					continue
				curr_system = get_system_by_name(ship["Location"], systems)
				#Go unexplored or go back
				dest = None
				for lane in curr_system["Hyperlanes"]:
					if lane not in observed:
						dest = lane
						break
				if dest == None:
					if ship["Name"] in ship_path and len(ship_path[ship["Name"]]) > 0:
						dest = ship_path[ship["Name"]].pop()
					else:
						continue
				else:
					if ship["Name"] not in ship_path:
						ship_path[ship["Name"]] = []
					ship_path[ship["Name"]].append(curr_system["Name"])
				sc.move(self.conn, ship, dest)
				self.state.add_update_ship(ship)



def get_accessable_systems(ships = [], systems = []):
	accessable = []
	for ship in ships:
		if ship["Location"] not in accessable:
			accessable.append(ship["Location"])
	for system in systems:
		if system["Name"] not in accessable:
			accessable.append(system["Name"])
		for lane in system["Hyperlanes"]:
			if lane not in accessable:
				accessable.append(lane)
	return accessable

def get_system_list(systems):
	l = []
	for system in systems:
		if system["Name"] not in l:
			l.append(system["Name"])
	return l

def get_system_by_name(name, systems):
	for system in systems:
		if name == system["Name"]:
			return system
	return None