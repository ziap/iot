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
from backend.modules.dashboard.devices_control.devices_models import (
	StateBuzzer,
	StateLed,
	StateRelay,
)
from pydantic import ValidationError
from backend.modules.auth.auth_controller import strip_prefix


async def handle_set_relay(request: Request) -> Response:
	if get_user(request) is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		state_relay = StateRelay(**payload)

		state = AppState.get(request)
		set_relay(state, state_relay.onRelay)

		return JSONResponse({"onRelay": state_relay.onRelay})

	except ValidationError as e:
		first_error = e.errors()[0]
		error_msg = first_error.get("msg", str(e))
		error_msg = strip_prefix(error_msg, "Value error, ")
		return Response(error_msg, status_code=400)


async def handle_set_buzzer(request: Request) -> Response:
	if get_user(request) is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		state_buzzer = StateBuzzer(**payload)

		state = AppState.get(request)
		set_buzzer(state, state_buzzer.onBuzzer)

		return JSONResponse({"onRelay": state_buzzer.onBuzzer})

	except ValidationError as e:
		first_error = e.errors()[0]
		error_msg = first_error.get("msg", str(e))
		error_msg = strip_prefix(error_msg, "Value error, ")
		return Response(error_msg, status_code=400)


async def handle_set_led_color(request: Request) -> Response:
	if get_user(request) is None:
		return Response(status_code=401)

	try:
		payload = await request.json()
		state_led = StateLed(**payload)

		state = AppState.get(request)
		set_led_color(state, state_led.ledColor)

		return JSONResponse({"onRelay": state_led.ledColor})

	except ValidationError as e:
		first_error = e.errors()[0]
		error_msg = first_error.get("msg", str(e))
		error_msg = strip_prefix(error_msg, "Value error, ")
		return Response(error_msg, status_code=400)


routes: list[BaseRoute] = [
	Route("/relay", handle_set_relay, methods=["POST"]),
	Route("/buzzer", handle_set_buzzer, methods=["POST"]),
	Route("/led", handle_set_led_color, methods=["POST"]),
]
