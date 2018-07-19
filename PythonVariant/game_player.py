import game_connection as gc

class GamePlayer:
	def __init__(self):
		self.conn = gc.GameSocketManager()
		self.ships = []
		self.systems = []

	def connect(self, host, port):
		self.conn.connect(host, port)

	def initialise(self):
		print("Establishing initial position...")
		cmd = gc.make_command("Ship", "List")
		data = self.conn.run_command(cmd)
		if data["Success"]:
			self.ships = data["ResultObject"]
			for ship in self.ships:
				print(ship["Name"] + " starts in " + ship["Location"])
		else:
			print("Something went horribly wrong")
			raise RuntimeError("Error from List command")

	def explore(self):
		print("Beginning to explore...")
		ship_path = {}
		accessable = self.get_accessable_systems()

		while len(self.systems) < len(accessable):
			#Observer the systems we're already in
			for ship in self.ships:
				if not self.system_observed(ship["Location"]):
					self.ship_observe(ship)
			#Have we touched everywhere
			if len(self.systems) != len(accessable):
				for ship in self.ships:
					curr_system = self.get_current_system(ship)
					#Go unexplored or go back
					dest = self.get_unexplored_system(curr_system["Hyperlanes"])
					if dest == None:
						if ship["Name"] in ship_path and len(ship_path[ship["Name"]]) > 0:
							dest = ship_path[ship["Name"]].pop()
						else:
							continue
					else:
						if ship["Name"] not in ship_path:
							ship_path[ship["Name"]] = []
						ship_path[ship["Name"]].append(curr_system["Name"])
					self.ship_move(ship, dest)
			#Have we finished yet?
			accessable = self.get_accessable_systems(accessable)
		print("Finished Exploring!")


	def get_accessable_systems(self, accessable = []):
		#Current ship locations are clearly accessable
		for ship in self.ships:
			if ship["Location"] not in accessable:
				accessable.append(ship["Location"])
		#Then check for any hyperlanes we know about
		for system in self.systems:
			for lane in system["Hyperlanes"]:
				if lane not in accessable:
					accessable.append(lane)
		return accessable

	def system_observed(self, system):
		for s in self.systems:
			if s["Name"] == system:
				return True
		return False

	def ship_observe(self, ship):
		cmd = gc.make_command("Ship", "Observe", ship["Name"])
		data = self.conn.run_command(cmd)
		if data["Success"]:
			system = data["ResultObject"]
			self.systems.append(system)
			print("Observed " + system["Name"])
			print("Stars:")
			for star in system["Stars"]:
				print("\t" + star["Name"])
			print("Planets:")
			for planet in system["Planets"]:
				print("\t" + planet["Name"])
			print("Hyperlanes")
			for lane in system["Hyperlanes"]:
				print("\t" + lane)
		else:
			raise RuntimeError("Observe command failed")

	def ship_move(self, ship, dest):
		cmd = gc.make_command("Ship", "Move", ship["Name"], [dest])
		data = self.conn.run_command(cmd)
		if data["Success"]:
			ship["Location"] = data["ResultObject"]["Location"]
			print("Moved " + ship["Name"] + " to " + ship["Location"])
		else:
			raise RuntimeError("Move command failed")

	def get_current_system(self, ship):
		for system in self.systems:
			if system["Name"] == ship["Location"]:
				return system
		raise RuntimeError("Ship not in system")

	def get_unexplored_system(self, systems):
		for system in systems:
			if not self.system_observed(system):
				return system
		return None