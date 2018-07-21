import game_connection as gc
import game_state as gs
import game_state_manager as gsm
import ship_commands as sc
import exploration_manager as em
import game_drawer as gd

class GamePlayer:
	def __init__(self):
		self.conn = gc.GameSocketManager()

	def connect(self, host, port):
		self.conn.connect(host, port)

	def initialise(self):
		print("Establishing initial position...")
		self.state = gs.GameState()
		state_man = gsm.StateManager(self.conn, self.state)
		state_man.start()
		return state_man

	def explore(self):
		ex_man = em.ExplorationManager(self.conn, self.state)
		ex_man.start()
		return ex_man

	def draw(self):
		drawer = gd.GameDrawer(self.state)
		drawer.start()
		return drawer