
import random

from models.check import CheckRequest, CheckResult


def resolve_check(request: CheckRequest) -> CheckResult:
    """
    Execute a D20 check.

    Dice generation and result calculation are
    controlled by Python, not by the AI model.
    """

    # 1. Generate a real D20 roll
    natural_roll = random.randint(1, 20)

    # 2. Calculate the final result
    total = natural_roll + request.modifier

    # 3. Compare against DC
    success = total >= request.dc

    # 4. Record special natural roll
    special_result = None

    if natural_roll == 20:
        special_result = "critical_success"

    elif natural_roll == 1:
        special_result = "critical_failure"

    # 5. Return structured result
    return CheckResult(
        natural_roll=natural_roll,
        modifier=request.modifier,
        dc=request.dc,
        total=total,
        success=success,
        special_result=special_result,
    )
