
from models.character import Character
from models.game_session import GameSession
from models.game_state import GameState
from models.game_save import GameSave


# 1. Create a character
character = Character(
    name="Test Hero",
    attributes={"strength": 3},
)

# 2. Create a game session
session = GameSession(
    session_id="test_session_001",
    world_id="test_world",
    world_version="1.0.0",
    character_id=character.character_id,
)

# 3. Create a matching game state
state = GameState(
    session_id="test_session_001",
    character=character,
)

# 4. Test valid save creation
save = GameSave(
    session=session,
    state=state,
)

assert save.session.session_id == save.state.session_id

print("Valid save creation: PASS")


# 5. Test mismatched session IDs
invalid_state = GameState(
    session_id="different_session",
    character=character,
)

try:
    GameSave(
        session=session,
        state=invalid_state,
    )
    raise AssertionError("Mismatched session IDs should be rejected.")
except ValueError:
    print("Mismatched session protection: PASS")


# 6. Test JSON serialization
save_json = save.model_dump_json()

assert isinstance(save_json, str)
assert "test_session_001" in save_json
assert "test_world" in save_json

print("Save JSON serialization: PASS")

print("All game save tests passed.")
