from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(max_length=200, examples=["Prepare campaign report"])
    description: str | None = Field(
        default=None,
        examples=["Compile the Q3 media campaign results"],
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must not be empty")
        return cleaned

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class TaskStatusUpdate(BaseModel):
    status: str = Field(examples=[TaskStatus.IN_PROGRESS.value])


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

