
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StateChangeProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    change_type: Literal[
        "character_attribute",
        "character_resource",
        "world_state",
        "scene_change",
        "fact_add",
    ]

    key: str | None = None

    value: str | int | float | bool | None = None

    reason: str = Field(
        min_length=1,
        description="Why this change is proposed"
    )

    source_action_id: str | None = None

