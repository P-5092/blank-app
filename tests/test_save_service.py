
from models.character import Character
from models.game_session import GameSession
from models.game_state import GameState
from models.game_save import GameSave

from services.save_service import restore_game


# 1. Create valid test data
character = Character(
    name="Restore Test Hero",
    attributes={"strength": 5},
)

session = GameSession(
    session_id="restore_test_001",
    world_id="test_world",
    world_version="1.0.0",
    character_id=character.character_id,
)

state = GameState(
    session_id=session.session_id,
    character=character,
)

save = GameSave(
    session=session,
    state=state,
)


# 2. Test normal restoration
restored_save, world = restore_game(save)

assert restored_save.session.session_id == session.session_id
assert world.world_id == "test_world"
assert world.version == "1.0.0"

print("Normal game restoration: PASS")


# 3. Test world version mismatch
wrong_version_session = session.model_copy(
    update={"world_version": "2.0.0"}
)

wrong_version_save = GameSave(
    session=wrong_version_session,
    state=state,
)

try:
    restore_game(wrong_version_save)
    raise AssertionError("World version mismatch should be rejected.")
except ValueError as error:
    assert "World version mismatch" in str(error)

print("World version protection: PASS")


# 4. Test character ID mismatch
wrong_character_session = session.model_copy(
    update={"character_id": "different_character"}
)

wrong_character_save = GameSave(
    session=wrong_character_session,
    state=state,
)

try:
    restore_game(wrong_character_save)
    raise AssertionError("Character ID mismatch should be rejected.")
except ValueError as error:
    assert "Saved character ID" in str(error)

print("Character ID protection: PASS")

print("All save restoration tests passed.")
