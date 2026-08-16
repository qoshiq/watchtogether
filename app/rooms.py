import secrets

from app.config import DEFAULT_VIDEO, ROOM_CODE_ALPHABET, ROOM_CODE_LENGTH

# In-memory room storage for V1.
# Keys are room codes; values are simple dicts with a "video" filename.
rooms: dict[str, dict[str, str]] = {}


def generate_room_code() -> str:
    """Generate a random, collision-resistant room code."""
    while True:
        code = "".join(
            secrets.choice(ROOM_CODE_ALPHABET) for _ in range(ROOM_CODE_LENGTH)
        )
        if code not in rooms:
            return code


def create_room(video: str = DEFAULT_VIDEO) -> str:
    """Create a room and return its code."""
    code = generate_room_code()
    rooms[code] = {"video": video}
    return code


def get_room(code: str) -> dict[str, str] | None:
    """Look up a room by code. Returns None if not found."""
    return rooms.get(code.upper())
