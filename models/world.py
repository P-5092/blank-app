
from pydantic import BaseModel, ConfigDict, Field

from models.world_rules import WorldRules


class World(BaseModel):
    """
    Represents a complete world package.
    """

    model_config = ConfigDict(extra="forbid")

    world_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    description: str = Field(default="")

    rules: WorldRules = Field(
        default_factory=WorldRules,
        description="Rules defined by this world",
    )



