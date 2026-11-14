
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class GameSession(BaseModel):
    """
    Single-player game session metadata.
    """

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    world_id: str = Field(min_length=1)

    world_version: str = Field(min_length=1)

    character_id: str = Field(min_length=1)

    status: str = "active"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

