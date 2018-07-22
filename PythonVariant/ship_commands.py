"""
Execute specifc commands for a ship
"""

import game_connection as gc
import game_constants as const

def move(conn, ship, dest):
	"""
	Order the ship to move to a destination
	"""
	cmd = gc.make_command(const.SHIP, const.MOVE, ship[const.NAME], [dest])
	data = conn.run_command(cmd)
	if data[const.SUCCESS]:
		ship[const.LOCATION] = data[const.RESULT_OBJECT][const.LOCATION]
		ship[const.STATUS] = data[const.RESULT_OBJECT][const.STATUS]
		print("Moving " + ship[const.NAME] + " to " + ship[const.LOCATION])
	else:
		print(data[const.MESSAGE])
		raise RuntimeError("Move command failed")

def observe(conn, ship):
	"""
	Observe the system that the ship is currently in
	"""
	cmd = gc.make_command(const.SHIP, const.OBSERVE, ship[const.NAME])
	data = conn.run_command(cmd)
	if data[const.SUCCESS]:
		system = data[const.RESULT_OBJECT]
		print("Observed " + system[const.NAME])
		print("Stars:")
		for star in system[const.STARS]:
			print("\t" + star[const.NAME])
		print("Planets:")
		for planet in system[const.PLANETS]:
			print("\t" + planet[const.NAME])
		print("Hyperlanes:")
		for lane in system[const.HYPERLANES]:
			print("\t" + lane)
		x_str = str(system[const.LOCATION][const.X])
		y_str = str(system[const.LOCATION][const.Y])
		print("Location: (" + x_str +  ", " + y_str + ")")
		return system
	print(data[const.MESSAGE])
	raise RuntimeError("Observe command failed")

def ship_list(conn):
	"""
	List all current ships
	"""
	cmd = gc.make_command(const.SHIP, const.LIST)
	data = conn.run_command(cmd)
	if data[const.SUCCESS]:
		ships = data[const.RESULT_OBJECT]
		for ship in ships:
			print(ship[const.NAME] + " is currently in " + ship[const.LOCATION])
		return ships
	print(data[const.MESSAGE])
	raise RuntimeError("List command failed")
