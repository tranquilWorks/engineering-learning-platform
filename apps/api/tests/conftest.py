from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.environ["ELP_COURSE_PATHS"] = str(ROOT / "courses")
os.environ.pop("ELP_WEB_DIST", None)
