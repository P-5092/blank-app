
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CheckRequest(BaseModel):
    """
    Input data for a D20 check.
    """

    model_config = ConfigDict(extra="forbid")

    modifier: int = 0

    dc: int = Field(
        ge=1,
        description="Difficulty Class"
    )


class CheckResult(BaseModel):
    """
    Final result of a D20 check.
    """

    model_config = ConfigDict(extra="forbid")

    natural_roll: int = Field(ge=1, le=20)

    modifier: int

    dc: int = Field(ge=1)

    total: int

    success: bool

    special_result: Literal[
        "critical_success",
        "critical_failure",
    ] | None = None
