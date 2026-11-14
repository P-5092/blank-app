
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AttributeDefinition(BaseModel):
    """
    Defines a numerical attribute in a world ruleset.
    """

    model_config = ConfigDict(extra="forbid")

    attribute_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(default="")


class ResourceDefinition(BaseModel):
    """
    Defines a numerical resource in a world ruleset.
    """

    model_config = ConfigDict(extra="forbid")

    resource_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(default="")

    initial_maximum: int = Field(ge=0)
    initial_current: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_initial_values(self):
        if self.initial_current > self.initial_maximum:
            raise ValueError(
                "Initial current resource cannot exceed initial maximum"
            )
        return self


class CheckRule(BaseModel):
    """
    Defines how a check is performed in a world.
    """

    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    attribute_id: str = Field(min_length=1)

    dice_type: Literal["d20"] = "d20"
    difficulty: int = Field(ge=1)

    description: str = Field(default="")


class ActionRule(BaseModel):
    """
    Defines how a type of player action should be assessed.
    """

    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1)
    name: str = Field(min_length=1)

    action_type: Literal["combat", "non_combat"]

    resolution_type: Literal[
        "direct_success",
        "requires_check",
        "rejected",
    ]

    check_rule_id: str | None = None

    description: str = Field(default="")

    @model_validator(mode="after")
    def validate_check_rule_reference(self):
        if self.resolution_type == "requires_check":
            if not self.check_rule_id:
                raise ValueError(
                    "A check_rule_id is required for actions requiring a check"
                )
        else:
            if self.check_rule_id is not None:
                raise ValueError(
                    "check_rule_id must be empty when no check is required"
                )

        return self


class WorldRules(BaseModel):
    """
    Contains all numerical and action rules defined by a world.
    """

    model_config = ConfigDict(extra="forbid")

    attributes: list[AttributeDefinition] = Field(default_factory=list)
    resources: list[ResourceDefinition] = Field(default_factory=list)
    check_rules: list[CheckRule] = Field(default_factory=list)
    action_rules: list[ActionRule] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_rules(self):
        attribute_ids = [
            item.attribute_id for item in self.attributes
        ]

        resource_ids = [
            item.resource_id for item in self.resources
        ]

        check_rule_ids = [
            item.rule_id for item in self.check_rules
        ]

        action_rule_ids = [
            item.rule_id for item in self.action_rules
        ]

        # Check duplicate IDs
        if len(attribute_ids) != len(set(attribute_ids)):
            raise ValueError("Duplicate attribute_id found")

        if len(resource_ids) != len(set(resource_ids)):
            raise ValueError("Duplicate resource_id found")

        if len(check_rule_ids) != len(set(check_rule_ids)):
            raise ValueError("Duplicate check rule ID found")

        if len(action_rule_ids) != len(set(action_rule_ids)):
            raise ValueError("Duplicate action rule ID found")

        # Check attribute references
        for rule in self.check_rules:
            if rule.attribute_id not in attribute_ids:
                raise ValueError(
                    f"Check rule references unknown attribute: "
                    f"{rule.attribute_id}"
                )

        # Check action rule references
        for rule in self.action_rules:
            if rule.resolution_type == "requires_check":
                if rule.check_rule_id not in check_rule_ids:
                    raise ValueError(
                        f"Action rule references unknown check rule: "
                        f"{rule.check_rule_id}"
                    )

        return self
