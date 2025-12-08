import asyncio
import json
import random
from datetime import datetime

from backend.models import SensorData
from backend.state import AppState


async def fetch_sensor_data() -> tuple[float, float]:
	"""
	Fetch sensor data from the hardware.
	Currently returns random data for testing purposes.
	Replace this function with actual sensor reading logic when ready.

	Returns:
		tuple[float, float]: (temperature, gas) readings
	"""
	# Simulate async sensor reading
	await asyncio.sleep(0.1)

	# Generate random sensor data
	temperature = round(random.uniform(18.0, 30.0), 2)
	gas = round(random.uniform(300.0, 500.0), 2)

	return temperature, gas


async def broadcast_sensor_data(
	state: AppState, data: dict[str, float | str | int]
) -> None:
	"""
	Broadcast sensor data to all connected WebSocket clients.
	Removes closed connections from the dictionary.
	"""
	closed_connections = []
	message = json.dumps(data)

	for hex_id, websocket in state.ws_connections.items():
		try:
			await websocket.send_text(message)
		except Exception as e:
			print(f"Failed to send to {hex_id}: {e}")
			closed_connections.append(hex_id)

	# Remove closed connections
	for hex_id in closed_connections:
		del state.ws_connections[hex_id]


async def poll_sensors(state: AppState) -> None:
	"""
	Poll sensors and store the data in the database.
	This function is called periodically by the sensor task.
	"""
	temperature, gas = await fetch_sensor_data()
	timestamp = datetime.now()

	with state.get_db() as db:
		sensor_data = SensorData(timestamp=timestamp, temperature=temperature, gas=gas)
		db.add(sensor_data)
		db.commit()

		# Get the ID after commit
		data_dict = {
			"id": sensor_data.id,
			"timestamp": timestamp.isoformat(),
			"temperature": temperature,
			"gas": gas,
		}

	# Broadcast to WebSocket clients
	await broadcast_sensor_data(state, data_dict)
