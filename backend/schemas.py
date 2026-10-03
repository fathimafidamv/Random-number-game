from enum import Enum
from pydantic import BaseModel, Field, model_validator


class GuessResult(str, Enum):
    SUCCESS = "SUCCESS"
    TOO_LOW = "TOO_LOW"
    TOO_HIGH = "TOO_HIGH"
    GAME_ALREADY_OVER = "GAME_ALREADY_OVER"


class PresetResponse(BaseModel):
    label: str = Field(..., description="Human-readable label for the preset, e.g. '1 to 20 (Medium)'")
    min_range: int = Field(..., description="Starting number")
    max_range: int = Field(..., description="Ending number")


class StartGameRequest(BaseModel):
    min_range: int = Field(default=1, description="Starting range number (minimum)")
    max_range: int = Field(default=100, description="Ending range number (maximum)")

    @model_validator(mode="after")
    def validate_range(self):
        if self.min_range >= self.max_range:
            raise ValueError("min_range must be strictly less than max_range.")
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "min_range": 1,
                "max_range": 20
            }
        }
    }


class StartGameResponse(BaseModel):
    game_id: str = Field(..., description="Unique UUID for this game session")
    min_range: int = Field(..., description="Selected minimum range")
    max_range: int = Field(..., description="Selected maximum range")
    message: str = Field(..., description="Welcome/status message")


class GuessRequest(BaseModel):
    game_id: str = Field(..., description="UUID of the active game session")
    guess: int = Field(..., description="The user's guessed number")

    model_config = {
        "json_schema_extra": {
            "example": {
                "game_id": "c8695029-4786-4ef5-bcf7-fc67ce0d96d9",
                "guess": 15
            }
        }
    }


class GuessResponse(BaseModel):
    game_id: str = Field(..., description="Game session UUID")
    guess: int = Field(..., description="The guess that was evaluated")
    result: GuessResult = Field(..., description="Result category: SUCCESS, TOO_LOW, TOO_HIGH, or GAME_ALREADY_OVER")
    message: str = Field(..., description="User-friendly feedback message")
    attempts: int = Field(..., description="Total attempts made so far")
    is_game_over: bool = Field(..., description="True if game has ended/won")
    secret_number: int | None = Field(default=None, description="Revealed only after winning or game over")


class GameHistoryItem(BaseModel):
    attempt: int = Field(..., description="Attempt sequence number")
    guess: int = Field(..., description="The number guessed")
    result: GuessResult = Field(..., description="Result category")
    message: str = Field(..., description="Feedback message given")


class GameStatusResponse(BaseModel):
    game_id: str = Field(..., description="Game session UUID")
    min_range: int = Field(..., description="Minimum range of the game")
    max_range: int = Field(..., description="Maximum range of the game")
    attempts: int = Field(..., description="Total attempts made so far")
    is_game_over: bool = Field(..., description="Whether the game has ended")
    history: list[GameHistoryItem] = Field(default_factory=list, description="List of previous attempts")
    secret_number: int | None = Field(default=None, description="Revealed if game is over")
