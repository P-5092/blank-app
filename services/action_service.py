
from models.action import PlayerAction
from models.resolution import ActionResolution
from models.check import CheckResult


def create_action_resolution(
    action: PlayerAction,
    outcome: str,
    description: str,
    check_result: CheckResult | None = None,
) -> ActionResolution:

    if outcome == "direct_success" and check_result is not None:
        raise ValueError(
            "Direct success cannot contain a check result"
        )

    if outcome == "check_success":
        if check_result is None or not check_result.success:
            raise ValueError(
                "Check success requires a successful check result"
            )

    if outcome == "check_failure":
        if check_result is None or check_result.success:
            raise ValueError(
                "Check failure requires a failed check result"
            )

    if outcome == "rejected" and check_result is not None:
        raise ValueError(
            "Rejected action cannot contain a check result"
        )

    return ActionResolution(
        action_id=action.action_id,
        outcome=outcome,
        description=description,
        check_result=check_result,
    )
