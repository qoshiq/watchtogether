from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import config, rooms

app = FastAPI(title=config.APP_NAME)

# Paths for templates and static assets.
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def video_path(filename: str) -> Path:
    """Resolve a video filename to an absolute path inside VIDEO_DIR."""
    # Prevent path traversal (e.g. "../../etc/passwd").
    safe_name = Path(filename).name
    return config.VIDEO_DIR / safe_name


def video_exists(filename: str) -> bool:
    path = video_path(filename)
    return path.is_file()


@app.get("/")
async def home(request: Request, error: str | None = None):
    """Render the home page with optional validation error."""
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "app_name": config.APP_NAME,
            "error": error,
        },
    )


@app.post("/rooms")
async def create_room():
    """Create a new room and redirect to it."""
    code = rooms.create_room()
    return RedirectResponse(url=f"/room/{code}", status_code=303)


@app.post("/rooms/join")
async def join_room(room_code: str = Form("")):
    """Validate a room code from the home page and redirect or show an error."""
    code = room_code.strip().upper()

    if not code:
        return RedirectResponse(url="/?error=empty_code", status_code=303)

    if rooms.get_room(code) is None:
        return RedirectResponse(url="/?error=not_found", status_code=303)

    return RedirectResponse(url=f"/room/{code}", status_code=303)


@app.get("/room/{room_code}")
async def room_page(request: Request, room_code: str):
    """Render the room page, or a not-found page if the room doesn't exist."""
    code = room_code.upper()
    room = rooms.get_room(code)

    if room is None:
        return templates.TemplateResponse(
            request,
            "room_not_found.html",
            {"app_name": config.APP_NAME, "room_code": code},
            status_code=404,
        )

    video_file = room["video"]
    missing_video = not video_exists(video_file)

    return templates.TemplateResponse(
        request,
        "room.html",
        {
            "app_name": config.APP_NAME,
            "room_code": code,
            "video_url": f"/videos/{video_file}" if not missing_video else None,
            "missing_video": missing_video,
            "video_file": video_file,
        },
    )


@app.get("/videos/{filename}")
async def serve_video(request: Request, filename: str):
    """Serve a video file with range-request support for seeking."""
    path = video_path(filename)

    if not path.is_file():
        return templates.TemplateResponse(
            request,
            "video_unavailable.html",
            {"app_name": config.APP_NAME, "video_file": filename},
            status_code=404,
        )

    # FileResponse handles HTTP Range headers for browser seeking.
    return FileResponse(
        path,
        media_type="video/mp4",
        filename=filename,
    )
