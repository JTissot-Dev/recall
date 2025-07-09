from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.core.utils import utc_now


class Role(str, Enum):
    user = "user"
    assistant = "assistant"


class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    role: Role = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=utc_now)

    conversation_id: UUID = Field(foreign_key="conversation.id")
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
