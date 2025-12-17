from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from json import JSONDecodeError
from starlette.routing import BaseRoute, Route

from backend.modules.auth.auth_service import get_user
from backend.modules.dashboard.devices_control.devices_service import (
	set_relay,
	set_buzzer,
	set_led_color,
)
from backend.state import AppState


async def handle_set_relay(request: Request) -> Response:
	if get_user(request) is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		on_relay = payload.get("onRelay")
		if on_relay is None:
			return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

		state = AppState.get(request)
		set_relay(state, on_relay)

		return JSONResponse({"onRelay": on_relay})

	except (JSONDecodeError, ValueError):
		return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)


async def handle_set_buzzer(request: Request) -> Response:
	if get_user(request) is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		on_buzzer = payload.get("onBuzzer")
		if on_buzzer is None:
			return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

		state = AppState.get(request)
		set_buzzer(state, on_buzzer)

		return JSONResponse({"onBuzzer": on_buzzer})

	except (JSONDecodeError, ValueError):
		return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)


async def handle_set_led_color(request: Request) -> Response:
	if get_user(request) is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		led_color = payload.get("ledColor")
		if led_color is None:
			return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

		state = AppState.get(request)
		set_led_color(state, led_color)

		return JSONResponse({"ledColor": led_color})

	except (JSONDecodeError, ValueError):
		return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)


routes: list[BaseRoute] = [
	Route("/relay", handle_set_relay, methods=["POST"]),
	Route("/buzzer", handle_set_buzzer, methods=["POST"]),
	Route("/led", handle_set_led_color, methods=["POST"]),
]
