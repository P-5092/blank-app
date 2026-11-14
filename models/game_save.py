
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, model_validator

from models.game_session import GameSession
from models.game_state import GameState


class GameSave(BaseModel):
    """
    A complete save package containing session metadata
    and authoritative runtime state.
    """

    model_config = ConfigDict(extra="forbid")

    save_version: str = "1.0"

    session: GameSession

    state: GameState

    saved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @model_validator(mode="after")
    def validate_session_consistency(self):
        if self.session.session_id != self.state.session_id:
            raise ValueError(
                "GameSession and GameState session IDs do not match."
            )

        return self
