import webbrowser
import threading
import time
import uvicorn

def open_browser():
    # Wait 1.5 seconds for the server to spin up, then open browser
    time.sleep(1.5)
    url = "https://random-number-game.onrender.com/play"
    print(f"\nOpening Game UI in browser: {url} ...")
    webbrowser.open(url)

if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Ensure backend folder is in Python path
    backend_dir = Path(__file__).resolve().parent / "backend"
    sys.path.insert(0, str(backend_dir))

    # Launch browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()

    print("=" * 55)
    print("  Starting Random Guessing Game Server...")
    print("  Game UI: https://random-number-game.onrender.com/play")
    print("  API Docs: https://random-number-game.onrender.com/docs")
    print("=" * 55)

