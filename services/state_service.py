
from copy import deepcopy
from datetime import datetime, timezone

from models.game_state import GameState
from models.state_change import StateChangeProposal
from services.resource_service import set_resource


def apply_state_change(
    state: GameState,
    proposal: StateChangeProposal,
) -> GameState:
    # Work on a copy so the original game state remains unchanged.
    new_state = deepcopy(state)

    if proposal.change_type == "character_attribute":
        key = proposal.key

        if not key or key not in new_state.character.attributes:
            raise ValueError(f"Unknown character attribute: {key}")

        old_value = new_state.character.attributes[key]

        if type(proposal.value) is not type(old_value):
            raise ValueError("Attribute value type does not match")

        new_state.character.attributes[key] = proposal.value

    elif proposal.change_type == "character_resource":
        key = proposal.key

        if not key or key not in new_state.character.resources:
            raise ValueError(f"Unknown character resource: {key}")

        if type(proposal.value) is not int:
            raise ValueError("Resource value must be an integer")

        old_resource = new_state.character.resources[key]

        new_state.character.resources[key] = set_resource(
            old_resource,
            proposal.value,
        )

    elif proposal.change_type == "world_state":
        if not proposal.key:
            raise ValueError("World state key cannot be empty")

        if proposal.value is None:
            raise ValueError("World state value cannot be None")

        new_state.world_state[proposal.key] = proposal.value

    elif proposal.change_type == "scene_change":
        if not isinstance(proposal.value, str):
            raise ValueError("Scene change value must be a string")

        if not proposal.value.strip():
            raise ValueError("Scene ID cannot be empty")

        new_state.current_scene_id = proposal.value

    elif proposal.change_type == "fact_add":
        if not isinstance(proposal.value, str):
            raise ValueError("Fact value must be a string")

        if not proposal.value.strip():
            raise ValueError("Fact cannot be empty")

        if proposal.value not in new_state.established_facts:
            new_state.established_facts.append(proposal.value)

    new_state.updated_at = datetime.now(timezone.utc)

    return new_state
