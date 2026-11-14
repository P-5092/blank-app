
from models.character import Character
from models.resource import Resource
from models.world import World


def create_character(
    world: World,
    name: str,
    attributes: dict[str, int],
) -> Character:
    """
    Create a character based on the definitions of a world.
    """

    # Get all attribute IDs defined by the world.
    expected_attribute_ids = {
        item.attribute_id
        for item in world.rules.attributes
    }

    provided_attribute_ids = set(attributes.keys())

    # Check for missing attributes.
    missing_attributes = (
        expected_attribute_ids - provided_attribute_ids
    )

    if missing_attributes:
        raise ValueError(
            f"Missing required attributes: "
            f"{sorted(missing_attributes)}"
        )

    # Check for undefined attributes.
    unknown_attributes = (
        provided_attribute_ids - expected_attribute_ids
    )

    if unknown_attributes:
        raise ValueError(
            f"Unknown attributes: "
            f"{sorted(unknown_attributes)}"
        )

    # Reject bool values, even though bool is a subclass of int.
    for attribute_id, value in attributes.items():
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                f"Attribute value must be an integer: {attribute_id}"
            )

    # Initialize resources from world definitions.
    resources = {
        item.resource_id: Resource(
            current=item.initial_current,
            maximum=item.initial_maximum,
        )
        for item in world.rules.resources
    }

    # Create the character.
    return Character(
        name=name,
        attributes=attributes,
        resources=resources,
    )
