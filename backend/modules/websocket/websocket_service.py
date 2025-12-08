import secrets
from datetime import datetime, timedelta, timezone
from os import environ as env

from jose import JWTError, jwt

secret_key = env.get("JWT_SECRET_KEY", default="secret-key")
ws_token_expire_min = int(env.get("WS_TOKEN_EXPIRE_MIN", default="60"))


def generate_ws_token() -> tuple[str, str]:
	"""
	Generate a WebSocket token with a random hex ID.

	Returns:
		tuple[str, str]: (token, hex_id)
	"""
	hex_id = secrets.token_hex(16)
	expire = datetime.now(timezone.utc) + timedelta(minutes=ws_token_expire_min)

	to_encode = {"ws_id": hex_id, "exp": expire}

	token = jwt.encode(to_encode, secret_key, algorithm="HS256")
	return token, hex_id


def verify_ws_token(token: str) -> str | None:
	"""
	Verify a WebSocket token and return the hex ID.

	Args:
		token: The JWT token to verify

	Returns:
		The hex ID if valid, None otherwise
	"""
	try:
		payload = jwt.decode(token, secret_key, algorithms=["HS256"])
		hex_id = payload.get("ws_id")
		if hex_id is None:
			return None
		return hex_id
	except JWTError:
		return None
