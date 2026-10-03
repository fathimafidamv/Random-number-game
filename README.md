# 🎯 Random Number Guessing Game (FastAPI Backend)

A complete Python backend using **FastAPI** and **Pydantic** for a range-based number guessing game.

---

## 🚀 Features

- **Custom & Preset Ranges**: Select `1 to 10`, `1 to 20`, `1 to 100`, or enter any custom `min_range` & `max_range`.
- **Validation with Pydantic**: Ensures valid range inputs (`min_range < max_range`) and data types.
- **Guess Counter**: Tracks the total number of attempts made in each game session.
- **Instant Result Feedback**:
  - `SUCCESS`: Correct guess (`🎉 Wow! It's correct!`)
  - `TOO_LOW`: If guess is less than secret number (`Your guess is less than my number`)
  - `TOO_HIGH`: If guess is greater than secret number (`Your guess is greater than my number`)
- **Session History**: Maintains full guess history per game session.
- **Interactive Web UI**: Ready-to-play frontend served at `/play`.
- **Swagger Documentation**: Interactive API testing available at `/docs`.

---

## 📦 Project Structure

```
random/
├── backend/
│   ├── main.py          # FastAPI application routes & game logic
│   ├── schemas.py       # Pydantic request/response models & validation
│   ├── app.py           # Alternate runner / entrypoint
│   └── requirements.txt # Project dependencies
├── frontend/
│   └── index.html       # Clean interactive web interface
└── README.md

```

---

## 🛠️ How to Run

### 1. Install Dependencies (if not already installed)
```bash
pip install fastapi uvicorn pydantic
```

### 2. Start the Backend Server
From the `backend` folder:
```bash
cd backend
python main.py
```
*Or using Uvicorn directly:*
```bash
uvicorn main:app --reload --port 8000
```

---

## 🌐 How to Use

1. **Play in Browser**: Open [http://127.0.0.1:8000/play](http://127.0.0.1:8000/play) in your web browser.
2. **Interactive API Docs (Swagger)**: Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📡 API Endpoints

### 1. Start a New Game
- **URL**: `POST /api/game/start`
- **Request Body**:
```json
{
  "min_range": 1,
  "max_range": 20
}
```
- **Response** (`201 Created`):
```json
{
  "game_id": "c8695029-4786-4ef5-bcf7-fc67ce0d96d9",
  "min_range": 1,
  "max_range": 20,
  "message": "Game started! A random number between 1 and 20 has been generated. Start guessing!"
}
```

---

### 2. Make a Guess
- **URL**: `POST /api/game/guess`
- **Request Body**:
```json
{
  "game_id": "c8695029-4786-4ef5-bcf7-fc67ce0d96d9",
  "guess": 8
}
```
- **Response** (When guess is lower):
```json
{
  "game_id": "c8695029-4786-4ef5-bcf7-fc67ce0d96d9",
  "guess": 8,
  "result": "TOO_LOW",
  "message": "Your guess is less than my number. Try higher! ⬆️",
  "attempts": 1,
  "is_game_over": false,
  "secret_number": null
}
```
- **Response** (When guess is correct):
```json
{
  "game_id": "c8695029-4786-4ef5-bcf7-fc67ce0d96d9",
  "guess": 15,
  "result": "SUCCESS",
  "message": "🎉 Wow!!!! It's correct! You guessed it in 2 attempt(s)!",
  "attempts": 2,
  "is_game_over": true,
  "secret_number": 15
}
```

---

### 3. Check Game Status & History
- **URL**: `GET /api/game/{game_id}`
- **Response**:
```json
{
  "game_id": "c8695029-4786-4ef5-bcf7-fc67ce0d96d9",
  "min_range": 1,
  "max_range": 20,
  "attempts": 2,
  "is_game_over": true,
  "history": [
    {
      "attempt": 1,
      "guess": 8,
      "result": "TOO_LOW",
      "message": "Your guess is less than my number. Try higher! ⬆️"
    },
    {
      "attempt": 2,
      "guess": 15,
      "result": "SUCCESS",
      "message": "🎉 Wow!!!! It's correct! You guessed it in 2 attempt(s)!"
    }
  ],
  "secret_number": 15
}
```
