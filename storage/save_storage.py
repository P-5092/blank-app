
import json
from pathlib import Path

from models.game_save import GameSave


SAVE_DIR = Path("data/saves")


def _get_save_path(session_id: str) -> Path:
    """
    Build a safe save file path using the session ID.
    """

    if not session_id or Path(session_id).name != session_id:
        raise ValueError("Invalid session ID.")

    if session_id in {".", ".."}:
        raise ValueError("Invalid session ID.")

    return SAVE_DIR / f"{session_id}.json"


def save_game(save: GameSave) -> Path:
    """
    Save a game using its session ID as the filename.

    Saving an existing session overwrites its previous save.
    """

    save_path = _get_save_path(save.session.session_id)

    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    save_path.write_text(
        save.model_dump_json(indent=4),
        encoding="utf-8",
    )

    return save_path


def load_game(session_id: str) -> GameSave:
    """
    Load and validate a save using its session ID.
    """

    save_path = _get_save_path(session_id)

    if not save_path.is_file():
        raise FileNotFoundError(
            f"Save file not found: {session_id}"
        )

    raw_data = json.loads(
        save_path.read_text(encoding="utf-8")
    )

    return GameSave.model_validate(raw_data)


def list_game_saves() -> list[str]:
    """
    List all saved session IDs.
    """

    if not SAVE_DIR.is_dir():
        return []

    return sorted(
        path.stem
        for path in SAVE_DIR.glob("*.json")
        if path.is_file()
    )

