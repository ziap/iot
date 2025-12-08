from datetime import datetime, timedelta

from backend.models import SensorData
from backend.state import AppState


def get_sensor_data(
	state: AppState, days: int = 3
) -> list[dict[str, float | str | int]]:
	n_days_ago = datetime.now() - timedelta(days=days)

	with state.get_db() as db:
		sensor_data = (
			db.query(SensorData)
			.filter(SensorData.timestamp >= n_days_ago)
			.order_by(SensorData.timestamp.desc())
			.all()
		)

		data_list = [
			{
				"id": data.id,
				"timestamp": data.timestamp.isoformat(),
				"temperature": data.temperature,
				"gas": data.gas,
			}
			for data in sensor_data
		]

	return data_list
