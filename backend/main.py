import random
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    StartGameRequest,
    StartGameResponse,
    GuessRequest,
    GuessResponse,
    GuessResult,
    GameStatusResponse,
    PresetResponse,
)

from fastapi.staticfiles import StaticFiles

DIST_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"
DIST_INDEX = DIST_DIR / "index.html"
VANILLA_INDEX = Path(__file__).resolve().parent.parent / "frontend" / "vanilla.html"

# ---------------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------------
app = FastAPI(
    title="Random Number Guessing Game API",
    description="FastAPI & Pydantic backend for range-based number guessing game.",
    version="1.0.0"
)

# Enable CORS so frontend (HTML/JS/React) can interact without issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount React static assets if built
if (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")


# ---------------------------------------------------------
# In-Memory Game Store
# ---------------------------------------------------------
# Structure: { game_id: { "secret_number": int, "min_range": int, "max_range": int, "attempts": int, "is_game_over": bool, "history": [] } }
games_db: dict[str, dict] = {}





# ---------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the Random Guessing Game API!",
        "play_in_browser": "/play",
        "docs_url": "/docs",
        "endpoints": {
            "play_game_ui": "GET /play",
            "start_game": "POST /api/game/start",
            "make_guess": "POST /api/game/guess",
            "game_status": "GET /api/game/{game_id}",
            "presets": "GET /api/game/presets"
        }
    }


@app.get("/play")
def play_game_ui():
    """Serves the interactive web UI directly in the browser."""
    if DIST_INDEX.exists():
        return FileResponse(DIST_INDEX)
    if VANILLA_INDEX.exists():
        return FileResponse(VANILLA_INDEX)
    raise HTTPException(status_code=404, detail="Frontend file not found.")




@app.get("/api/game/presets", response_model=list[PresetResponse])
def get_presets():

    """Returns standard range options for the user to choose from."""
    return [
        {"label": "1 to 10 (Easy)", "min_range": 1, "max_range": 10},
        {"label": "1 to 20 (Medium)", "min_range": 1, "max_range": 20},
        {"label": "1 to 100 (Hard)", "min_range": 1, "max_range": 100},
    ]



@app.post("/api/game/start", response_model=StartGameResponse, status_code=status.HTTP_201_CREATED)
def start_game(payload: StartGameRequest):
    """
    Start a new guessing game with the selected range (e.g. 1 to 10, 1 to 20, 1 to 100).
    A random number is generated and hidden in server memory.
    """
    game_id = str(uuid.uuid4())
    secret_number = random.randint(payload.min_range, payload.max_range)

    games_db[game_id] = {
        "secret_number": secret_number,
        "min_range": payload.min_range,
        "max_range": payload.max_range,
        "attempts": 0,
        "is_game_over": False,
        "history": []
    }

    return StartGameResponse(
        game_id=game_id,
        min_range=payload.min_range,
        max_range=payload.max_range,
        message=f"Game started! A random number between {payload.min_range} and {payload.max_range} has been generated. Start guessing!"
    )


@app.post("/api/game/guess", response_model=GuessResponse)
def make_guess(payload: GuessRequest):
    """
    Submit a guess for an active game session.
    Checks:
    - If guess == secret_number: SUCCESS / Wow it's correct!
    - If guess < secret_number: TOO_LOW / Your guess is less than my number
    - If guess > secret_number: TOO_HIGH / Your guess is greater than my number
    Counts total guesses.
    """
    game = games_db.get(payload.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game session not found. Please start a new game.")

    if game["is_game_over"]:
        return GuessResponse(
            game_id=payload.game_id,
            guess=payload.guess,
            result="GAME_ALREADY_OVER",
            message=f"Game is already over! The correct number was {game['secret_number']}.",
            attempts=game["attempts"],
            is_game_over=True,
            secret_number=game["secret_number"]
        )

    # Increment guess count
    game["attempts"] += 1
    current_attempt = game["attempts"]
    secret = game["secret_number"]

    # Determine result
    if payload.guess == secret:
        result = "SUCCESS"
        message = f"🎉 Wow!!!! It's correct! You guessed it in {current_attempt} attempt(s)!"
        game["is_game_over"] = True
        revealed_secret = secret
    elif payload.guess < secret:
        result = "TOO_LOW"
        message = "Your guess is less than my number. Try higher! ⬆️"
        revealed_secret = None
    else:
        result = "TOO_HIGH"
        message = "Your guess is greater than my number. Try lower! ⬇️"
        revealed_secret = None

    # Save to history
    game["history"].append({
        "attempt": current_attempt,
        "guess": payload.guess,
        "result": result,
        "message": message
    })

    return GuessResponse(
        game_id=payload.game_id,
        guess=payload.guess,
        result=result,
        message=message,
        attempts=current_attempt,
        is_game_over=game["is_game_over"],
        secret_number=revealed_secret
    )


@app.get("/api/game/{game_id}", response_model=GameStatusResponse)
def get_game_status(game_id: str):
    """Retrieve the current status and guess history of a game."""
    game = games_db.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game session not found.")

    return GameStatusResponse(
        game_id=game_id,
        min_range=game["min_range"],
        max_range=game["max_range"],
        attempts=game["attempts"],
        is_game_over=game["is_game_over"],
        history=game["history"],
        secret_number=game["secret_number"] if game["is_game_over"] else None
    )


if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server at http://127.0.0.1:8000 ...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
