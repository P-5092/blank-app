
import json
from pathlib import Path

from models.world import World


WORLDS_DIR = Path("data/worlds")


def load_world(world_id: str) -> World:
    """
    Load and validate a world package by its ID.
    """

    if not world_id or Path(world_id).name != world_id:
        raise ValueError("Invalid world ID")

    file_path = WORLDS_DIR / f"{world_id}.json"

    if not file_path.is_file():
        raise FileNotFoundError(
            f"World package not found: {world_id}"
        )

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    world = World.model_validate(data)

    if world.world_id != world_id:
        raise ValueError(
            "World ID in file does not match requested world ID"
        )

    return world
