import threading as th
import game_connection as gc
import time as t

class StateManager(th.Thread):
	def __init__(self, conn, state):
		self.conn = conn
		self.state = state
		self.active = False
		super().__init__()

	def run(self):
		cmd = gc.make_command("State", "Poll")
		self.active = True
		while self.active:
			data = self.conn.run_command(cmd)
			if data["Success"]:
				state = data["ResultObject"]
				self.update_state(state)
			else:
				raise RuntimeError("State polling failed!")
			t.sleep(0.1)

	def update_state(self, state):
		for ship in state["Ships"]:
			self.state.add_update_ship(ship)
		for system in state["SolarSystems"]:
			self.state.add_update_system(system)