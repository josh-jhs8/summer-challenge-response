"""
Create an object to represent the state of the game
"""

import copy as c
import threading as t
import game_constants as const

class GameState:
	"""
	Class to represent the current state of the game.
	Manages concurreny as well.
	"""
	def __init__(self):
		self.player = {}
		self.systems = []
		self.lock = t.Lock()

	def get_systems(self):
		"""
		Gets the systems based on the current state
		"""
		self.lock.acquire(True)
		new_systems = c.deepcopy(self.systems)
		self.lock.release()
		return new_systems

	def get_ships(self):
		"""
		Gets the players ships based on the current state
		"""
		self.lock.acquire(True)
		new_ships = []
		if self.player:
			new_ships = c.deepcopy(self.player[const.SHIPS])
		self.lock.release()
		return new_ships

	def add_update_system(self, system):
		"""
		Adds a system to the state if not present,
		updates the system if already present
		"""
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
		"""
		Adds a ship to the state if not present,
		updates the ship if already present
		"""
		if not self.player:
			raise RuntimeError("Don't even have player yet!")
		new_ship = c.deepcopy(ship)
		self.lock.acquire(True)
		update = False
		for s_ship in self.player[const.SHIPS]:
			if s_ship[const.NAME] == new_ship[const.NAME]:
				update = True
				s_ship[const.LOCATION] = new_ship[const.LOCATION]
				s_ship[const.STATUS] = new_ship[const.STATUS]
		if not update:
			self.player[const.SHIPS].append(new_ship)
		self.lock.release()

	def add_update_player(self, player):
		"""
		Adds a player to state if not present,
		updates the player if already present
		"""
		if not self.player:
			self.lock.acquire(True)
			self.player[const.NAME] = player[const.NAME]
			self.player[const.SHIPS] = []
			self.lock.release()
		for ship in player[const.SHIPS]:
			self.add_update_ship(ship)
