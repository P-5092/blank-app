
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from models.resource import Resource


class Character(BaseModel):
    model_config = ConfigDict(extra="forbid")

    character_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    name: str = Field(
        min_length=1,
        description="Character name"
    )

    attributes: dict[str, int] = Field(
        default_factory=dict,
        description="Character numerical attributes"
    )

    resources: dict[str, Resource] = Field(
        default_factory=dict,
        description="Character numerical resources"
    )

