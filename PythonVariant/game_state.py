import copy as c
import threading as t

class GameState:
	def __init__(self, ships = [], systems = []):
		self.ships = c.deepcopy(ships)
		self.systems = c.deepcopy(systems)
		self.lock = t.Lock()

	def get_systems(self):
		self.lock.acquire(True)
		new_systems = c.deepcopy(self.systems)
		self.lock.release()
		return new_systems

	def get_ships(self):
		self.lock.acquire(True)
		new_ships = c.deepcopy(self.ships)
		self.lock.release()
		return new_ships

	def add_update_system(self, system):
		new_system = c.deepcopy(system)
		self.lock.acquire(True)
		update = False
		for sys in self.systems:
			if sys["Name"] == new_system["Name"]:
				update = True
				sys["Stars"] = new_system["Stars"]
				sys["Planets"] = new_system["Planets"]
				sys["Hyperlanes"] = new_system["Hyperlanes"]
				sys["Location"] = new_system["Location"]
		if not update:
			self.systems.append(new_system)
		self.lock.release()

	def add_update_ship(self, ship):
		new_ship = c.deepcopy(ship)
		self.lock.acquire(True)
		update = False
		for s in self.ships:
			if s["Name"] == new_ship["Name"]:
				update = True
				s["Location"] = new_ship["Location"]
		if not update:
			self.ships.append(new_ship)
		self.lock.release()

