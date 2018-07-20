import game_player as gp

def play_game(host, port):
	player = gp.GamePlayer()
	player.connect(host, port)
	player.initialise()
	player.explore()
	#player.draw()

def quick():
	play_game("localhost", 2092)