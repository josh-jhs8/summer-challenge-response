"""
Manages a sinlge player a all there available actions
"""

import game_connection as gc
import game_state as gs
import game_state_manager as gsm
import exploration_manager as em
import game_drawer as gd


class GamePlayer:
    """
    Class represent game player and their available action threads
    """

    def __init__(self):
        self.conn = gc.GameSocketManager()
        self.state = None

    def connect(self, host, port):
        """
        Connect to challenge server
        """
        self.conn.connect(host, port)

    def initialise(self):
        """
        Initialise the state of the challenge
        """
        print("Establishing initial position...")
        self.state = gs.GameState()
        state_man = gsm.StateManager(self.conn, self.state)
        state_man.start()
        return state_man

    def explore(self):
        """
        Explore the challenge provided
        """
        ex_man = em.ExplorationManager(self.conn, self.state)
        ex_man.start()
        return ex_man

    def draw(self):
        """
        Draw the state of the challenge
        """
        drawer = gd.GameDrawer(self.state)
        drawer.start()
        return drawer
