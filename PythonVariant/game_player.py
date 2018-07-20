import game_connection as gc
import game_state as gs
import ship_commands as sc
import exploration_manager as em
#import pygame as pg

class GamePlayer:
	def __init__(self):
		self.conn = gc.GameSocketManager()

	def connect(self, host, port):
		self.conn.connect(host, port)

	def initialise(self):
		print("Establishing initial position...")
		ships = sc.list(self.conn)
		self.state = gs.GameState(ships)

	def explore(self):
		ex_man = em.ExplorationManager(self.conn, self.state)
		ex_man.explore()

'''
	def draw(self):
		screen = pg.display.set_mode((640, 480))
		screen.fill((0, 0, 0))
		for system in self.systems:
			self.draw_lines_for_system(screen, system)
		pg.display.flip()

	def draw_lines_for_system(self, screen, system):
		origin = self.get_point_from_system(system)
		for lane in system["Hyperlanes"]:
			new_sys = self.get_system_by_name(lane)
			dest = self.get_point_from_system(new_sys)
			pg.draw.line(screen, (255, 255, 255), origin, dest)

	def get_point_from_system(self, system):
		loc = system["Location"]
		return ((loc["X"]*100)+200, (loc["Y"]*100)+200)

	def get_system_by_name(self, name):
		for system in self.systems:
			if system["Name"] == name:
				return system
		raise RuntimeError("No such system found")
'''