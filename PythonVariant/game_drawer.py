"""
Module to draw a game state as it develops

We're going to assume all coordinates are between -10 and + 10
We are also going to convert from normal to pygame coordinates
"""

import threading as t
import pygame as pg
import exploration_manager as em
import game_constants as const

SIZE = WIDTH, HEIGHT = 640, 480
UNIT_DX = WIDTH / 21
UNIT_DY = HEIGHT / 21
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
WHITE = 255, 255, 255


class GameDrawer(t.Thread):
    """
    Class to create thread for drawing game state
    """

    def __init__(self, state):
        self.state = state
        super().__init__()

    def run(self):
        """
        Start the drawing thread
        """
        screen = pg.display.set_mode(SIZE)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:  # pylint: disable=E1101
                    pg.display.quit()
                    pg.quit()  # pylint: disable=E1101
                    return
            self.draw(screen)

    def draw(self, screen):
        """
        Draw a single frame
        """
        screen.fill(BLACK)
        ships = self.state.get_ships()
        systems = self.state.get_systems()
        draw_systems(screen, systems)
        draw_ships(screen, ships, systems)
        pg.display.flip()


def draw_ships(screen, ships, systems):
    """
    Draw the ships on to the surface
    """
    for ship in ships:
        sys = em.get_system_by_name(ship[const.LOCATION], systems)
        if sys:
            pos = translate_position(sys[const.LOCATION])
            pg.draw.circle(screen, RED, pos, int(3))


def draw_systems(screen, systems):
    """
    Draw the systems and hyperlanes onto the surface
    """
    for system in systems:
        pos = translate_position(system[const.LOCATION])
        for lane in system[const.HYPERLANES]:
            new_sys = em.get_system_by_name(lane, systems)
            if new_sys:
                new_pos = translate_position(new_sys[const.LOCATION])
                pg.draw.line(screen, WHITE, pos, new_pos)
        pg.draw.circle(screen, GREEN, pos, int(5))


def translate_position(loc):
    """
    Translate the challenge location into coordinates for pygame
    """
    return (int(round((loc[const.X] + 11) * UNIT_DX)),
            int(round((loc[const.Y] - 11) * UNIT_DY) * -1))
