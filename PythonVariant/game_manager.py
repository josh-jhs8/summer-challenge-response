"""
Play challenge game
"""

import time as t
import game_player as gp

def play_game(host, port):
	"""
	Play game on specific remote endpoint
	"""
	player = gp.GamePlayer()
	player.connect(host, port)
	state_man = player.initialise()
	tasks = []
	tasks.append(player.explore())
	tasks.append(player.draw())
	is_alive = True
	while is_alive:
		is_alive = False
		for task in tasks:
			if task.is_alive():
				is_alive = True
		t.sleep(1)
	state_man.active = False

def quick():
	"""
	Quick access to standard game game location
	"""
	play_game("localhost", 2092)

if __name__ == "__main__":
	quick()
