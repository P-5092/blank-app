
from models.game_save import GameSave
from models.world import World

from services.world_service import load_world


def restore_game(save: GameSave) -> tuple[GameSave, World]:
    """
    Restore a saved game using its original world version.

    The current world package must match both the saved
    world ID and version.
    """

    session = save.session

    world = load_world(session.world_id)

    if world.version != session.world_version:
        raise ValueError(
            "World version mismatch: "
            f"save requires {session.world_version}, "
            f"but loaded world is {world.version}."
        )

    if save.state.session_id != session.session_id:
        raise ValueError(
            "Game session and game state IDs do not match."
        )

    if save.state.character.character_id != session.character_id:
        raise ValueError(
            "Saved character ID does not match session metadata."
        )

    return save, world
