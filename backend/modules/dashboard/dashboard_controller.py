from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import BaseRoute, Route

from backend.modules.auth.auth_service import get_user


async def handle_dashboard(request: Request) -> Response:
	user = get_user(request)
	if user is None:
		return Response("Unauthenticated", status_code=304)

	return JSONResponse(
		{
			"username": user.email,
		}
	)


routes: list[BaseRoute] = [Route("/", handle_dashboard, methods=["GET"])]
