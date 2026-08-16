from pathlib import Path

# Project root is one level above the app package.
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory where video files are stored on disk.
VIDEO_DIR = BASE_DIR / "videos"

# Default video assigned to newly created rooms.
DEFAULT_VIDEO = "sample.mp4"

# Room codes use this many characters.
ROOM_CODE_LENGTH = 5

# Characters used for room codes (no 0/O, 1/I/L to avoid confusion).
ROOM_CODE_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

APP_NAME = "WatchTogether"
