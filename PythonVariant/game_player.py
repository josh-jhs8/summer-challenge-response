import game_connection as gc
import game_state as gs
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
		ships = sc.list(self.conn)
		self.state = gs.GameState(ships)

	def explore(self):
		ex_man = em.ExplorationManager(self.conn, self.state)
		ex_man.start()
		return ex_man

	def draw(self):
		drawer = gd.GameDrawer(self.state)
		drawer.start()
		return drawer