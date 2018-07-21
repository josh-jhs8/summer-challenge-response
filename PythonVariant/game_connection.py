import socket
import threading
import json
import game_constants as const

class GameSocketManager:
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
		self.lock = threading.Lock()

	def connect(self, host, port):
		self.sock.connect((host, port))

	def run_command(self, cmd):
		msg = json.dumps(cmd)
		self.lock.acquire(True)
		sent = self.sock.send(msg.encode("utf-8"))
		if sent == 0:
			raise RuntimeError("connection broken")
		response = self.sock.recv(1000000)
		self.lock.release()
		msg = response.decode("utf-8")
		return json.loads(msg)

def make_command(cmd_type, action, subject = "", arguments = []):
	return { const.TYPE: cmd_type, const.SUBJECT: subject, const.ACTION: action, const.ARGUMENTS: arguments}