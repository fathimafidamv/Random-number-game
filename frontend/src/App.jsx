import React, { useState } from 'react';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  // ----------------------------------------------------
  // 1. STATE VARIABLES (Beginner friendly useState hooks)
  // ----------------------------------------------------
  const [minRange, setMinRange] = useState(1);
  const [maxRange, setMaxRange] = useState(10);
  
  // Game session states
  const [gameStarted, setGameStarted] = useState(false);
  const [gameId, setGameId] = useState("");
  const [guessInput, setGuessInput] = useState("");
  
  // Game feedback states
  const [attempts, setAttempts] = useState(0);
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(""); // "TOO_LOW", "TOO_HIGH", "SUCCESS"
  const [isGameOver, setIsGameOver] = useState(false);
  const [history, setHistory] = useState([]); // List of past guesses

  // ----------------------------------------------------
  // 2. FUNCTION: Start a New Game
  // ----------------------------------------------------
  async function startGame() {
    if (minRange >= maxRange) {
      alert("Min number must be less than Max number!");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/game/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ min_range: minRange, max_range: maxRange })
      });

      const data = await response.json();

      // Reset state for new game
      setGameId(data.game_id);
      setGameStarted(true);
      setAttempts(0);
      setMessage("Game Started! Make your first guess.");
      setResult("");
      setIsGameOver(false);
      setHistory([]);
      setGuessInput("");
    } catch (error) {
      alert("Error: Backend is not running! Please run python main.py first.");
    }
  }

  // ----------------------------------------------------
  // 3. FUNCTION: Submit a Guess
  // ----------------------------------------------------
  async function submitGuess(e) {
    if (e) e.preventDefault();

    if (!guessInput) {
      alert("Please enter a number!");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/game/guess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          game_id: gameId,
          guess: parseInt(guessInput, 10)
        })
      });

      const data = await response.json();

      // Update feedback from backend
      setAttempts(data.attempts);
      setMessage(data.message);
      setResult(data.result);
      setIsGameOver(data.is_game_over);

      // Add to history list
      setHistory(prev => [
        {
          attempt: data.attempts,
          guess: data.guess,
          result: data.result
        },
        ...prev
      ]);

      // Clear input box
      setGuessInput("");
    } catch (error) {
      alert("Failed to submit guess to backend.");
    }
  }

  // ----------------------------------------------------
  // 4. FUNCTION: Reset / Play Again
  // ----------------------------------------------------
  function resetGame() {
    setGameStarted(false);
    setMessage("");
    setResult("");
    setAttempts(0);
    setHistory([]);
  }

  // ----------------------------------------------------
  // 5. USER INTERFACE (JSX)
  // ----------------------------------------------------
  return (
    <div className="container">
      <h1>🎯 Number Guessing Game</h1>
      <p className="subtitle">React & FastAPI Beginner Project</p>

      {/* VIEW 1: RANGE SELECTION (Before Game Starts) */}
      {!gameStarted ? (
        <div className="card">
          <h3>Select Range:</h3>
          
          {/* Preset Buttons */}
          <div className="preset-buttons">
            <button
              className={maxRange === 10 ? "active" : ""}
              onClick={() => { setMinRange(1); setMaxRange(10); }}
            >
              1 to 10
            </button>
            <button
              className={maxRange === 20 ? "active" : ""}
              onClick={() => { setMinRange(1); setMaxRange(20); }}
            >
              1 to 20
            </button>
            <button
              className={maxRange === 100 ? "active" : ""}
              onClick={() => { setMinRange(1); setMaxRange(100); }}
            >
              1 to 100
            </button>
          </div>

          {/* Custom Range Inputs */}
          <div className="custom-range">
            <label>
              Min:
              <input
                type="number"
                value={minRange}
                onChange={(e) => setMinRange(parseInt(e.target.value, 10) || 0)}
              />
            </label>
            <span>to</span>
            <label>
              Max:
              <input
                type="number"
                value={maxRange}
                onChange={(e) => setMaxRange(parseInt(e.target.value, 10) || 0)}
              />
            </label>
          </div>

          <button className="primary-btn" onClick={startGame}>
            Start Game 🚀
          </button>
        </div>
      ) : (
        /* VIEW 2: ACTIVE GAME (After Game Starts) */
        <div className="card">
          <div className="stats">
            <span>Range: <strong>{minRange} - {maxRange}</strong></span>
            <span>Total Guesses: <strong>{attempts}</strong></span>
          </div>

          {/* Guess Form */}
          <form onSubmit={submitGuess} className="guess-form">
            <input
              type="number"
              placeholder="Enter your guess"
              value={guessInput}
              disabled={isGameOver}
              onChange={(e) => setGuessInput(e.target.value)}
              autoFocus
            />
            <button type="submit" className="primary-btn" disabled={isGameOver}>
              Guess
            </button>
          </form>

          {/* Feedback Message (Too Low, Too High, Success) */}
          {message && (
            <div className={`message-box ${result}`}>
              {message}
            </div>
          )}

          {/* Past Guesses History */}
          {history.length > 0 && (
            <div className="history">
              <h4>History:</h4>
              <ul>
                {history.map((item, index) => (
                  <li key={index} className="history-item">
                    <span>Attempt #{item.attempt}: <strong>{item.guess}</strong></span>
                    <span className={`badge ${item.result}`}>{item.result.replace("_", " ")}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Restart Button */}
          <button className="secondary-btn" onClick={resetGame}>
            🔄 Change Range / Restart
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
