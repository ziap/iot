from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from json import JSONDecodeError
from starlette.routing import BaseRoute, Route

from backend.modules.auth.auth_service import get_user
from backend.state import AppState


async def handle_set_relay(request: Request) -> Response:
	"""Implement relay control signal from web"""
	user = get_user(request)
	if user is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		on_relay: bool = payload.get("onRelay")
		if on_relay is None:
			return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)
		else:
			state = AppState.get(request)
			state.mqtt_client.publish("relay", on_relay, qos=2)

	except (JSONDecodeError, ValueError):
		return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

	return JSONResponse({"on_relay": payload})


async def handle_set_buzzer(request: Request) -> Response:
	"""Implement buzzer control signal from web"""
	user = get_user(request)
	if user is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		on_buzzer: bool = payload.get("onBuzzer")
		if on_buzzer is None:
			return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)
		else:
			state = AppState.get(request)
			state.mqtt_client.publish("buzzer", on_buzzer, qos=2)

	except (JSONDecodeError, ValueError):
		return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

	return JSONResponse({"on_buzzer": payload})


async def handle_set_led_color(request: Request) -> Response:
	"""Display LEDcolor by data from web"""
	user = get_user(request)
	if user is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		led_color: bool = payload.get("ledColor")
		if led_color is None:
			return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)
		else:
			state = AppState.get(request)
			state.mqtt_client.publish("led", led_color, qos=2)

	except (JSONDecodeError, ValueError):
		return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

	return JSONResponse({"led_color": payload})


routes: list[BaseRoute] = [
	Route("/relay", handle_set_relay, methods=["POST"]),
	Route("/buzzer", handle_set_buzzer, methods=["POST"]),
	Route("/led", handle_set_led_color, methods=["POST"]),
]
