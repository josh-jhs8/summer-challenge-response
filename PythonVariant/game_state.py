import copy as c
import threading as t
import game_constants as const

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
			if sys[const.NAME] == new_system[const.NAME]:
				update = True
				sys[const.STARS] = new_system[const.STARS]
				sys[const.PLANETS] = new_system[const.PLANETS]
				sys[const.HYPERLANES] = new_system[const.HYPERLANES]
				sys[const.LOCATION] = new_system[const.LOCATION]
		if not update:
			self.systems.append(new_system)
		self.lock.release()

	def add_update_ship(self, ship):
		new_ship = c.deepcopy(ship)
		self.lock.acquire(True)
		update = False
		for s in self.ships:
			if s[const.NAME] == new_ship[const.NAME]:
				update = True
				s[const.LOCATION] = new_ship[const.LOCATION]
				s[const.STATUS] = new_ship[const.STATUS]
		if not update:
			self.ships.append(new_ship)
		self.lock.release()

