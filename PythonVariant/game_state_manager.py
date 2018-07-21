import threading as th
import game_connection as gc
import time as t
import game_constants as const

class StateManager(th.Thread):
	def __init__(self, conn, state):
		self.conn = conn
		self.state = state
		self.active = False
		super().__init__()

	def run(self):
		cmd = gc.make_command(const.STATE, const.POLL)
		self.active = True
		while self.active:
			data = self.conn.run_command(cmd)
			if data[const.SUCCESS]:
				state = data[const.RESULT_OBJECT]
				self.update_state(state)
			else:
				raise RuntimeError("State polling failed!")
			t.sleep(0.1)

	def update_state(self, state):
		for ship in state[const.SHIPS]:
			self.state.add_update_ship(ship)
		for system in state[const.SYSTEMS]:
			self.state.add_update_system(system)