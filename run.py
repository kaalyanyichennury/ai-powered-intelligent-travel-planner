"""
Multi-process runner for AI-Powered Intelligent Travel Planner.
Launches both FastAPI Backend (port 8000) and Vite React Frontend (port 5173).
"""

import os
import sys
import subprocess
import time
import signal

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def main():
    print("=" * 70)
    print("🚀 STARTING AI-POWERED INTELLIGENT TRAVEL PLANNER")
    print("   Machine Learning • LLM • RAG • 6-Agent AI Architecture")
    print("=" * 70)

    # 1. Start FastAPI Backend
    print("\n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", "backend.app.main:app",
        "--host", "127.0.0.1", "--port", "8000"
    ]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=ROOT_DIR,
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    # Give backend a moment to bind port
    time.sleep(2)

    # 2. Start React Vite Frontend
    print("\n[2/2] Starting React Vite Frontend on http://localhost:5173 ...")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_cmd = [npm_cmd, "run", "dev"]
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=FRONTEND_DIR,
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    print("\n" + "=" * 70)
    print("🌟 SYSTEM OPERATIONAL!")
    print("   👉 Web Application UI: http://localhost:5173")
    print("   👉 FastAPI Swagger API: http://127.0.0.1:8000/docs")
    print("   👉 Press Ctrl+C at any time to safely stop both servers.")
    print("=" * 70 + "\n")

    def shutdown_handler(sig, frame):
        print("\nStopping AI Travel Planner servers...")
        try:
            backend_proc.terminate()
            frontend_proc.terminate()
        except Exception:
            pass
        print("Shutdown complete. Goodbye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("Backend process exited.")
                break
            if frontend_proc.poll() is not None:
                print("Frontend process exited.")
                break
    except KeyboardInterrupt:
        shutdown_handler(None, None)

if __name__ == "__main__":
    main()
