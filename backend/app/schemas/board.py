from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BoardCreate(BaseModel):
    name: str = Field(max_length=150, examples=["Q3 Website Refresh"])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name must not be empty")
        return cleaned


class BoardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime

