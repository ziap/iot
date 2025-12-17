from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute, Route

from backend.modules.auth.auth_service import get_user
from backend.modules.chat.chat_service import chat
from backend.state import AppState


async def handle_chat(request: Request) -> Response:
	user = get_user(request)
	if user is None:
		return Response(status_code=401)

	try:
		body = await request.json()
		messages = body.get("messages", [])

		if not messages:
			return JSONResponse({"error": "No messages provided"}, status_code=400)

		state = AppState.get(request)
		new_messages = chat(state, messages)

		return JSONResponse({"messages": new_messages})

	except Exception as e:
		return JSONResponse({"error": str(e)}, status_code=500)


routes: list[BaseRoute] = [
	Route("/", handle_chat, methods=["POST"]),
]
