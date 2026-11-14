
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Resource(BaseModel):
    """
    A numerical resource with current and maximum values.
    """

    model_config = ConfigDict(extra="forbid")

    current: int = Field(ge=0)
    maximum: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_current_value(self):
        if self.current > self.maximum:
            raise ValueError(
                "Current resource cannot exceed maximum"
            )
        return self
