
from models.resource import Resource


def change_resource(
    resource: Resource,
    amount: int,
) -> Resource:
    """
    Increase or decrease the current resource value.

    Positive amount: increase.
    Negative amount: decrease.
    """

    new_current = resource.current + amount

    new_current = max(
        0,
        min(new_current, resource.maximum)
    )

    return Resource(
        current=new_current,
        maximum=resource.maximum,
    )


def set_resource(
    resource: Resource,
    value: int,
) -> Resource:
    """
    Set the current resource value directly.
    """

    if value < 0 or value > resource.maximum:
        raise ValueError(
            "Resource value must be between 0 and maximum"
        )

    return Resource(
        current=value,
        maximum=resource.maximum,
    )


def set_resource_maximum(
    resource: Resource,
    new_maximum: int,
    preserve_current: bool = True,
) -> Resource:
    """
    Change the maximum resource value.

    If preserve_current is True, current value is kept
    unless it exceeds the new maximum.

    If preserve_current is False, current value is set
    to the new maximum.
    """

    if new_maximum < 0:
        raise ValueError(
            "Maximum resource cannot be negative"
        )

    if preserve_current:
        new_current = min(
            resource.current,
            new_maximum
        )
    else:
        new_current = new_maximum

    return Resource(
        current=new_current,
        maximum=new_maximum,
    )
