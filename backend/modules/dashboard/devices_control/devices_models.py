from pydantic import BaseModel
from typing import Literal


class StateBuzzer(BaseModel):
	"""State Buzzer"""

	onBuzzer: bool


class StateRelay(BaseModel):
	"""State Relay"""

	onRelay: bool


class StateLed(BaseModel):
	"""State Led"""

	ledColor: Literal["red", "yellow", "green"]
