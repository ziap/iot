from starlette.routing import BaseRoute, WebSocketRoute
from starlette.websockets import WebSocket, WebSocketDisconnect

from backend.modules.websocket.websocket_service import verify_ws_token
from backend.state import AppState


async def websocket_endpoint(websocket: WebSocket) -> None:
	"""
	WebSocket endpoint for real-time sensor data updates.

	Query parameters:
		token: JWT token containing the WebSocket connection ID
	"""
	await websocket.accept()

	# Get and verify token from query params
	token = websocket.query_params.get("token")
	if not token:
		await websocket.close(code=1008, reason="Missing token")
		return

	hex_id = verify_ws_token(token)
	if not hex_id:
		await websocket.close(code=1008, reason="Invalid token")
		return

	# Get app state and register connection
	state = AppState.get(websocket)
	state.ws_connections[hex_id] = websocket

	try:
		# Keep connection alive and listen for close
		while True:
			# Wait for any message (we don't process them, just keep alive)
			await websocket.receive_text()
	except WebSocketDisconnect:
		# Remove connection when closed
		if hex_id in state.ws_connections:
			del state.ws_connections[hex_id]
	except Exception as e:
		print(f"WebSocket error for {hex_id}: {e}")
		if hex_id in state.ws_connections:
			del state.ws_connections[hex_id]


routes: list[BaseRoute] = [WebSocketRoute("/ws", websocket_endpoint)]
