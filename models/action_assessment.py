

from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class ActionAssessment(BaseModel):
    """
    Records the rule-based assessment of a player action.
    """

    model_config = ConfigDict(extra="forbid")

    action_id: str = Field(min_length=1)

    matched_rule_id: str | None = None

    decision: Literal[
        "direct_success",
        "requires_check",
        "rejected",
    ]

    reason: str = Field(min_length=1)

    check_attribute: str | None = None

    dc: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def validate_check_requirements(self):

        if self.decision == "requires_check":
            if not self.check_attribute:
                raise ValueError(
                    "A check attribute is required"
                )

            if self.dc is None:
                raise ValueError(
                    "DC is required when a check is needed"
                )

        else:
            if self.check_attribute is not None or self.dc is not None:
                raise ValueError(
                    "Check parameters must be empty "
                    "when no check is required"
                )

        return self
