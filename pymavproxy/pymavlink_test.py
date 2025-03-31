from pymavlink import mavutil


def request_message(connection, msg_id):
	message = connection.mav.command_long_encode(
		connection.target_system,  # Target system ID
		connection.target_component,  # Target component ID
		mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,  # ID of command to send
		0,  # Confirmation
		msg_id,  # param1: Message ID to be requested
		0, # param2: Unused
		0, # param3: Unused
		0, # param4: Unused
		0, # param5: Unused
		0, # param6: Unused
		0, # param7: Unused
		)
	# Send the COMMAND_LONG
	connection.mav.send(message)

	# Wait for a response (blocking) to the MAV_CMD_SET_MESSAGE_INTERVAL command and print result
	response = connection.recv_match(type='COMMAND_ACK', blocking=True)
	if response:
		if response.command == mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE:
			if response.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
				return True
	return False

def set_message_interval(connection, msg_id, interval_us):
	message = connection.mav.command_long_encode(
		connection.target_system,  # Target system ID
		connection.target_component,  # Target component ID
		mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # ID of command to send
		0,  # Confirmation
		msg_id,  # param1: Message ID to be streamed
		interval_us, # param2: Interval in microseconds
		0, # param3: Unused
		0, # param4: Unused
		0, # param5: Unused
		0, # param6: Unused
		0, # param7: Unused
		)
	# Send the COMMAND_LONG
	connection.mav.send(message)

	# Wait for a response (blocking) to the MAV_CMD_SET_MESSAGE_INTERVAL command and print result
	response = connection.recv_match(type='COMMAND_ACK', blocking=True)
	if response:
		if response.command == mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL:
			if response.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
				return True
	return False

# Start a connection listening on a UDP port
connection = mavutil.mavlink_connection('/dev/ttyACM0')

# Wait for the first heartbeat to set the system and component ID of remote system for the link
connection.wait_heartbeat()
print(f"Heartbeat from system (system {connection.target_system} component {connection.target_component})")

result = set_message_interval(connection, mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS, 1e6)
print("Command accepted" if result else "Command failed")


while True:
	msg = connection.recv_match(blocking=True)
	if not msg:
		pass
	elif msg.get_type() == "BAD_DATA":
		if mavutil.all_printable(msg.data):
			sys.stdout.write(msg.data)
			sys.stdout.flush()
	else:
		#Message is valid
		if msg.get_type() == "SYS_STATUS":
			print(msg.__dict__)
			#print(msg._fieldnames)
			print(msg.battery_remaining)
			#exit()
