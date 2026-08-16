# WatchTogether

A simple watch-party web application. Create a room, share the code with friends, and watch a video together.

**V1 scope:** create a room, join a room, watch a video. No chat, sync, auth, or calls yet.

## Features (V1)

- Create a room with a unique short code
- Join an existing room by code
- Watch a configured video in the browser (HTML5 `<video>`)
- Dark-themed, responsive UI
- In-memory room storage (no database)

## Requirements

- Python 3.10 or newer
- A virtual environment (recommended)

## Installation

```bash
cd watchtogether
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Place video files in the `videos/` directory. A `sample.mp4` is included for testing.

## Running

Start the development server from the project root:

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Quick test flow

1. Click **Create Room** — you are redirected to `/room/<code>`.
2. Copy the room code (button on the room page).
3. Open a private/incognito window, go to the home page, and **Join Room** with that code.
4. Both windows show the same video; playback is independent per browser.

## Project structure

```text
watchtogether/
├── app/
│   ├── main.py          # FastAPI routes and app setup
│   ├── rooms.py         # In-memory room storage and code generation
│   ├── config.py        # Paths and settings
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # CSS and JavaScript
├── videos/              # Video files served by the backend
├── requirements.txt
└── README.md
```

## Current limitations

V1 intentionally does **not** include:

- Persistent rooms (restart clears all rooms)
- Authentication
- Synchronized playback
- Real-time chat
- Voice or video calls
- WebSockets

These are planned for future versions (V2+).

## Configuration

Edit `app/config.py` to change:

- `VIDEO_DIR` — directory for video files
- `DEFAULT_VIDEO` — filename assigned to new rooms
- `ROOM_CODE_LENGTH` — length of generated room codes
