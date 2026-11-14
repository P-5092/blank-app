
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from models.character import Character


class GameState(BaseModel):
    """
    Authoritative runtime state of a game.
    """

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)

    character: Character

    current_scene_id: str | None = None

    world_state: dict[str, object] = Field(
        default_factory=dict
    )

    established_facts: list[str] = Field(
        default_factory=list
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
