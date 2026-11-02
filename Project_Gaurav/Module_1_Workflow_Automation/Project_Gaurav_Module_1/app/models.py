from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class LeadInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=254)
    phone: str = Field(..., min_length=10, max_length=15)
    company: str = Field(..., min_length=2, max_length=150)
    requirement: str = Field(..., min_length=2, max_length=500)

    @field_validator("name", "company", "requirement")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank.")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Please provide a valid email address.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        value = re.sub(r"[\s\-()+]", "", value.strip())
        if not re.fullmatch(r"\d{10,15}", value):
            raise ValueError("Phone must contain 10 to 15 digits.")
        return value
