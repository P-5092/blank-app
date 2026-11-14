
from models.action import PlayerAction
from models.check import CheckRequest
from models.game_state import GameState
from models.resolution import ActionResolution
from models.world import World

from services.action_assessment_service import assess_action
from services.action_service import create_action_resolution
from services.check_service import resolve_check


def process_action(
    world: World,
    state: GameState,
    action: PlayerAction,
) -> ActionResolution:
    """
    Process a player action through assessment, optional check,
    and final resolution.

    This service does not modify the game state.
    """

    # Step 1: Assess the action using world rules.
    assessment = assess_action(world, action)

    # Step 2: Handle rejected actions.
    if assessment.decision == "rejected":
        return create_action_resolution(
            action=action,
            outcome="rejected",
            description=assessment.reason,
        )

    # Step 3: Handle direct success.
    if assessment.decision == "direct_success":
        return create_action_resolution(
            action=action,
            outcome="direct_success",
            description=assessment.reason,
        )

    # Step 4: Resolve an action requiring a check.
    if assessment.decision == "requires_check":

        attribute_id = assessment.check_attribute

        if attribute_id not in state.character.attributes:
            raise ValueError(
                f"Character is missing required attribute: {attribute_id}"
            )

        modifier = state.character.attributes[attribute_id]

        check_request = CheckRequest(
            modifier=modifier,
            dc=assessment.dc,
        )

        check_result = resolve_check(check_request)

        # Step 5: Convert the check result into an action resolution.
        if check_result.success:
            outcome = "check_success"
        else:
            outcome = "check_failure"

        description = (
            f"{assessment.reason} "
            f"Check result: {check_result.total} "
            f"against DC {check_result.dc}."
        )

        return create_action_resolution(
            action=action,
            outcome=outcome,
            description=description,
            check_result=check_result,
        )

    raise ValueError(
        f"Unsupported action assessment decision: {assessment.decision}"
    )
