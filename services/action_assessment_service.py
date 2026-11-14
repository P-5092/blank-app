
from models.action import PlayerAction
from models.action_assessment import ActionAssessment
from models.world import World


def assess_action(
    world: World,
    action: PlayerAction,
) -> ActionAssessment:
    """
    Assess a player action using the rules defined by the world.
    """

    candidate_rule_id = action.candidate_rule_id

    # A candidate rule ID is required.
    if not candidate_rule_id:
        return ActionAssessment(
            action_id=action.action_id,
            decision="rejected",
            reason="No candidate action rule was provided.",
        )

    # Find the exact action rule.
    action_rule = next(
        (
            rule
            for rule in world.rules.action_rules
            if rule.rule_id == candidate_rule_id
        ),
        None,
    )

    # Reject unknown rules.
    if action_rule is None:
        return ActionAssessment(
            action_id=action.action_id,
            decision="rejected",
            reason=f"Unknown action rule: {candidate_rule_id}",
        )

    # Validate action type.
    if action.action_type != action_rule.action_type:
        return ActionAssessment(
            action_id=action.action_id,
            decision="rejected",
            reason="Action type does not match the world rule.",
        )

    # Handle direct success.
    if action_rule.resolution_type == "direct_success":
        return ActionAssessment(
            action_id=action.action_id,
            matched_rule_id=action_rule.rule_id,
            decision="direct_success",
            reason=action_rule.description or action_rule.name,
        )

    # Handle rejected rules.
    if action_rule.resolution_type == "rejected":
        return ActionAssessment(
            action_id=action.action_id,
            matched_rule_id=action_rule.rule_id,
            decision="rejected",
            reason=action_rule.description or action_rule.name,
        )

    # Handle actions requiring a check.
    check_rule = next(
        (
            rule
            for rule in world.rules.check_rules
            if rule.rule_id == action_rule.check_rule_id
        ),
        None,
    )

    if check_rule is None:
        raise ValueError(
            f"Referenced check rule not found: "
            f"{action_rule.check_rule_id}"
        )

    return ActionAssessment(
        action_id=action.action_id,
        matched_rule_id=action_rule.rule_id,
        decision="requires_check",
        reason=action_rule.description or action_rule.name,
        check_attribute=check_rule.attribute_id,
        dc=check_rule.difficulty,
    )
