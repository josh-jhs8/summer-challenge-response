"""
Manage the state of the game
"""
import threading as th
import time as t
import game_connection as gc
import game_constants as const


class StateManager(th.Thread):
    """
    Thread class for continually polling the game state
    """

    def __init__(self, conn, state):
        self.conn = conn
        self.state = state
        self.active = False
        super().__init__()

    def run(self):
        """
        Run the polling thread
        """
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
        """
        Update the state of the game based on the returned state
        """
        if not state[const.PLAYERS]:
            raise RuntimeError("No players in state")
        self.state.add_update_player(state[const.PLAYERS][0])
        for system in state[const.SYSTEMS]:
            self.state.add_update_system(system)
