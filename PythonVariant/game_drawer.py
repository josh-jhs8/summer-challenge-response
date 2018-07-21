import pygame as pg
import threading as t
import exploration_manager as em
import game_constants as const

'''
We're going to assume all coordinates are between -10 and + 10
We are also going to convert from normal to pygame coordinates
'''

size = width, height = 640, 480
unit_dx = width / 21
unit_dy = height / 21
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255

class GameDrawer(t.Thread):
	def __init__(self, state):
		self.state = state
		super().__init__()

	def run(self):
		screen = pg.display.set_mode(size)
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.display.quit()
					pg.quit()
					return
			self.draw(screen)

	def draw(self, screen):
		screen.fill(black)
		ships = self.state.get_ships()
		systems = self.state.get_systems()
		self.draw_systems(screen, systems)
		self.draw_ships(screen, ships, systems)
		pg.display.flip()

	def draw_ships(self, screen, ships, systems):
		for ship in ships:
			sys = em.get_system_by_name(ship[const.LOCATION], systems)
			if sys:
				pos = translate_position(sys[const.LOCATION])
				pg.draw.circle(screen, red, pos, int(3))

	def draw_systems(self, screen, systems):
		for system in systems:
			pos = translate_position(system[const.LOCATION])
			for lane in system[const.HYPERLANES]:
				new_sys = em.get_system_by_name(lane, systems)
				if new_sys:
					new_pos = translate_position(new_sys[const.LOCATION])
					pg.draw.line(screen, white, pos, new_pos)
			pg.draw.circle(screen, green, pos, int(5))


def translate_position(loc):
	return (int(round((loc[const.X]+11)*unit_dx)), int(round((loc[const.Y]-11)*unit_dy)*-1))