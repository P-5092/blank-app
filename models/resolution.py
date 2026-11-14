
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from models.check import CheckResult


class ActionResolution(BaseModel):
    """
    Records the program's judgment of a player action.
    """

    model_config = ConfigDict(extra="forbid")

    resolution_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    action_id: str = Field(
        min_length=1
    )

    outcome: Literal[
        "direct_success",
        "check_success",
        "check_failure",
        "rejected",
    ]

    description: str = Field(
        min_length=1,
        description="Explanation of the action resolution"
    )

    check_result: CheckResult | None = None
