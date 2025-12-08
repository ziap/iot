from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute, Route

from backend.modules.auth.auth_service import get_user
from backend.state import AppState, start_task
from backend.tasks.poll_sensors import poll_sensors


async def handle_get_poll_status(request: Request) -> Response:
	"""Get the polling task status"""
	user = get_user(request)
	if user is None:
		return Response(status_code=401)

	state = AppState.get(request)
	is_polling = state.sensor_task is not None

	return JSONResponse({"is_polling": is_polling})


async def handle_toggle_polling(request: Request) -> Response:
	"""Toggle the polling task on/off"""
	user = get_user(request)
	if user is None:
		return Response(status_code=401)

	state = AppState.get(request)

	if state.sensor_task is None:
		# Start polling
		state.sensor_task = start_task(
			lambda: poll_sensors(state),
			interval=3.0,  # Poll every 3 seconds
		)
		is_polling = True
	else:
		# Stop polling
		state.sensor_task.cancel()
		state.sensor_task = None
		is_polling = False

	return JSONResponse(
		{
			"is_polling": is_polling,
			"message": f"Polling {'started' if is_polling else 'stopped'}",
		}
	)


routes: list[BaseRoute] = [
	Route("/status", handle_get_poll_status, methods=["GET"]),
	Route("/toggle", handle_toggle_polling, methods=["POST"]),
]
