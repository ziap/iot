from typing import Literal

from pydantic import BaseModel


class StateBuzzer(BaseModel):
	"""State Buzzer"""

	onBuzzer: bool


class StateRelay(BaseModel):
	"""State Relay"""

	onRelay: bool


class StateLed(BaseModel):
	"""State Led"""

	ledColor: Literal["red", "yellow", "green"]
