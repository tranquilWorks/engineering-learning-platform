#!/usr/bin/env python3
"""Run the API and Vite development servers with shared shutdown handling."""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(command: str) -> None:
    if shutil.which(command) is None:
        raise SystemExit(f"required command not found: {command}")


def main() -> int:
    require("npm")
    require(sys.executable)
    environment = os.environ.copy()
    environment.setdefault("ELP_COURSE_PATHS", str(ROOT / "courses"))
    environment.setdefault("ELP_DEV_CORS", "http://localhost:5173")
    environment["PYTHONPATH"] = str(ROOT / "apps" / "api" / "src")

    commands = [
        [sys.executable, "-m", "uvicorn", "elp_api.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        ["npm", "run", "dev:web"],
    ]
    processes = [subprocess.Popen(command, cwd=ROOT, env=environment) for command in commands]

    stopping = False

    def stop(*_: object) -> None:
        nonlocal stopping
        if stopping:
            return
        stopping = True
        for process in processes:
            if process.poll() is None:
                process.terminate()

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    try:
        while not stopping:
            for process in processes:
                code = process.poll()
                if code is not None:
                    stop()
                    return code
            time.sleep(0.2)
    finally:
        stop()
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
