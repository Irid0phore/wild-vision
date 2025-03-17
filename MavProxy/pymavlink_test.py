from pymavlink import mavutil


def set_message_interval(connection, msg_id, interval_us):
	# Define command_long_encode message to send MAV_CMD_SET_MESSAGE_INTERVAL command
	# param1: Message to stream
	# param2: Stream interval in microseconds
	message = connection.mav.command_long_encode(
		connection.target_system,  # Target system ID
		connection.target_component,  # Target component ID
		mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # ID of command to send
		0,  # Confirmation
		msg_id,  # param1: Message ID to be streamed
		interval_us, # param2: Interval in microseconds
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
connection = mavutil.mavlink_connection('udpin:localhost:5762')

# Wait for the first heartbeat to set the system and component ID of remote system for the link
connection.wait_heartbeat()
print(f"Heartbeat from system (system {connection.target_system} component {connection.target_component})")

result = set_message_interval(connection, mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS, 1e6)
print("Command accepted" if result else "Command failed")

msg = m.recv_match(type='SYS_STATUS',blocking=True)
if not msg:
	exit()
if msg.get_type() == "BAD_DATA":
	if mavutil.all_printable(msg.data):
		sys.stdout.write(msg.data)
		sys.stdout.flush()
else:
	#Message is valid
	# Use the attribute
	print('Mode: %s' % msg.mode)