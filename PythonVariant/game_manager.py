import game_player as gp

def play_game(host, port):
	player = gp.GamePlayer()
	player.connect(host, port)
	player.initialise()
	player.explore()