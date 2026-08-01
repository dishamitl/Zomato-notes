from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime


# ---------- User Schemas ----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty or whitespace.")
        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Note Schemas ----------

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1)
    tag: str | None = None
    owner_id: int


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    content: str | None = Field(default=None, min_length=1)
    tag: str | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tag: str | None
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)