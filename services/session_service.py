
from models.character import Character
from models.world import World
from models.game_session import GameSession


def create_game_session(
    world: World,
    character: Character
) -> GameSession:
    """
    Create a game session using a validated World
    and Character object.
    """

    session = GameSession(
        world_id=world.world_id,
        world_version=world.version,
        character_id=character.character_id,
    )

    return session
