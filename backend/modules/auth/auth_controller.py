from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Route

from backend.models import User
from backend.state import AppState

from .auth_models import UserCreate, UserLogin
from .auth_service import authenticate, hash_create, hash_verify, logout


def strip_prefix(text: str, prefix: str) -> str:
	"""Remove prefix from text if present, otherwise return text unchanged."""
	if text.startswith(prefix):
		return text[len(prefix) :]
	return text


async def handle_register(request: Request) -> Response:
	state = AppState.get(request)
	with state.get_db() as db:
		try:
			payload = await request.json()
			user_create = UserCreate(**payload)
			password_hash = hash_create(user_create.password)
			user_db = User(
				email=user_create.email,
				password_hash=password_hash,
			)

			db.add(user_db)
			db.commit()
			db.refresh(user_db)

			return authenticate(user_db)
		except ValidationError as e:
			# Extract first error message from pydantic validation error
			first_error = e.errors()[0]
			error_msg = first_error.get("msg", str(e))
			error_msg = strip_prefix(error_msg, "Value error, ")
			return Response(error_msg, status_code=400)
		except IntegrityError:
			db.rollback()
			return Response("Username or email already registered", status_code=400)


async def handle_login(request: Request) -> Response:
	state = AppState.get(request)
	with state.get_db() as db:
		try:
			payload = await request.json()
			user_login = UserLogin(**payload)

			user = db.query(User).filter((User.email == user_login.email)).first()

			if user is None:
				return Response("Wrong username or password", status_code=401)

			if not hash_verify(user_login.password, str(user.password_hash)):
				return Response("Wrong username or password", status_code=401)

			return authenticate(user)

		except ValidationError as e:
			# Extract first error message from pydantic validation error
			first_error = e.errors()[0]
			error_msg = first_error.get("msg", str(e))
			error_msg = strip_prefix(error_msg, "Value error, ")
			return Response(error_msg, status_code=400)


async def handle_logout(_: Request) -> Response:
	return logout()


routes: list[BaseRoute] = [
	Route("/register", handle_register, methods=["POST"]),
	Route("/login", handle_login, methods=["POST"]),
	Route("/logout", handle_logout, methods=["POST"]),
]
