
from models.game_state import GameState
from models.resolution import ActionResolution
from models.state_change import StateChangeProposal
from services.state_service import apply_state_change


def apply_action_effects(
    state: GameState,
    resolution: ActionResolution,
    proposals: list[StateChangeProposal],
) -> GameState:
    """
    Apply explicitly provided state change proposals
    associated with an action resolution.

    This service does not generate action effects.
    It only validates their source and applies them.

    The original state remains unchanged if any proposal fails.
    """

    # Rejected actions cannot produce state changes.
    if resolution.outcome == "rejected" and proposals:
        raise ValueError(
            "Rejected actions cannot produce state changes."
        )

    # No proposals means no state changes.
    if not proposals:
        return state

    # Validate all proposal sources before applying any changes.
    for proposal in proposals:
        if proposal.source_action_id != resolution.action_id:
            raise ValueError(
                "State change proposal source action ID "
                "does not match the action resolution."
            )

    # Apply changes to a working copy.
    new_state = state

    for proposal in proposals:
        new_state = apply_state_change(
            new_state,
            proposal,
        )

    return new_state
