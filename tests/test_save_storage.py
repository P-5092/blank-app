
from storage.save_storage import (
    save_game,
    load_game,
    list_game_saves,
)

from models.character import Character
from models.game_session import GameSession
from models.game_state import GameState
from models.game_save import GameSave


# 1. Create test data
character = Character(
    name="Storage Test Hero",
    attributes={
        "strength": 5,
        "agility": 3,
    },
)

session = GameSession(
    session_id="storage_test_002",
    world_id="test_world",
    world_version="1.0.0",
    character_id=character.character_id,
)

state = GameState(
    session_id=session.session_id,
    character=character,
    current_scene_id="forest_entrance",
)

save = GameSave(
    session=session,
    state=state,
)


# 2. Test saving
save_path = save_game(save)

assert save_path.exists()
assert save_path.name == "storage_test_002.json"

print("Save file creation: PASS")


# 3. Test loading
loaded_save = load_game("storage_test_002")

assert loaded_save.session.session_id == session.session_id
assert loaded_save.state.character.name == "Storage Test Hero"
assert loaded_save.state.current_scene_id == "forest_entrance"

print("Save file loading: PASS")


# 4. Test overwriting an existing save
updated_state = state.model_copy(
    update={"current_scene_id": "dark_forest"}
)

updated_save = GameSave(
    session=session,
    state=updated_state,
)

save_game(updated_save)

reloaded_save = load_game("storage_test_002")

assert reloaded_save.state.current_scene_id == "dark_forest"

print("Save overwrite: PASS")


# 5. Test listing saves
save_ids = list_game_saves()

assert "storage_test_002" in save_ids
assert save_ids == sorted(save_ids)

print("Save listing: PASS")


# 6. Test missing save
try:
    load_game("nonexistent_session_999")
    raise AssertionError("Missing save should be rejected.")
except FileNotFoundError:
    print("Missing save protection: PASS")


# 7. Test invalid session ID
try:
    load_game("../invalid_session")
    raise AssertionError("Invalid session ID should be rejected.")
except ValueError:
    print("Invalid session ID protection: PASS")


print("All save storage tests passed.")

