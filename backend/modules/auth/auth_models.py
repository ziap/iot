from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
	"""User creation schema"""

	email: EmailStr
	password: str
	confirm_password: str

	@field_validator("password")
	@classmethod
	def validate_password(cls, v: str) -> str:
		# Check password length (using unicode character count)
		pwd_length = len(v)
		if pwd_length < 8 or pwd_length > 32:
			raise ValueError("Password must be between 8 and 32 characters long")

		# Define criteria checks
		criterias = [
			any(c.isupper() for c in v),  # uppercase letter
			any(c.islower() for c in v),  # lowercase letter
			any(c.isdigit() for c in v),  # numeric digit
			any(not c.isalnum() and not c.isspace() for c in v),  # special character
		]

		criteria_names = [
			"uppercase letter",
			"lowercase letter",
			"numeric digit",
			"special character",
		]

		# Check each criteria and raise specific error message
		for criteria_met, criteria_name in zip(criterias, criteria_names):
			if not criteria_met:
				raise ValueError(f"Password must contain at least one {criteria_name}")

		return v

	@field_validator("confirm_password")
	@classmethod
	def passwords_match(cls, v, info):
		if "password" in info.data and v != info.data["password"]:
			raise ValueError("Passwords do not match")
		return v


class UserLogin(BaseModel):
	"""User login schema"""

	email: EmailStr
	password: str
