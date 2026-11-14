
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class PlayerAction(BaseModel):
    """
    Structured representation of a player action.
    """

    model_config = ConfigDict(extra="forbid")

    action_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    raw_input: str = Field(
        min_length=1,
        description="Original player input"
    )

    intent: str = Field(
        min_length=1,
        description="What the player intends to do"
    )

    target: str | None = None

    method: str | None = None

    action_type: Literal[
        "combat",
        "non_combat",
    ]

    expected_outcome: str | None = None

    candidate_rule_id: str | None = None
