import game_connection as gc

def move(conn, ship, dest):
	cmd = gc.make_command("Ship", "Move", ship["Name"], [dest])
	data = conn.run_command(cmd)
	if data["Success"]:
		ship["Location"] = data["ResultObject"]["Location"]
		print("Moved " + ship["Name"] + " to " + ship["Location"])
	else:
		raise RuntimeError("Move command failed")

def observe(conn, ship):
	cmd = gc.make_command("Ship", "Observe", ship["Name"])
	data = conn.run_command(cmd)
	if data["Success"]:
		system = data["ResultObject"]
		print("Observed " + system["Name"])
		print("Stars:")
		for star in system["Stars"]:
			print("\t" + star["Name"])
		print("Planets:")
		for planet in system["Planets"]:
			print("\t" + planet["Name"])
		print("Hyperlanes:")
		for lane in system["Hyperlanes"]:
			print("\t" + lane)
		print("Location: (" + str(system["Location"]["X"]) + ", " + str(system["Location"]["Y"]) + ")")
		return system
	else:
		raise RuntimeError("Observe command failed")

def list(conn):
	cmd = gc.make_command("Ship", "List")
	data = conn.run_command(cmd)
	if data["Success"]:
		ships = data["ResultObject"]
		for ship in ships:
			print(ship["Name"] + " starts in " + ship["Location"])
		return ships
	else:
		raise RuntimeError("List command failed")