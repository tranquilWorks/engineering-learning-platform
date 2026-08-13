from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd


def jsonable(value: Any) -> Any:
    """Convert numerical result objects to JSON-safe values without hiding complex data."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, np.generic):
        return jsonable(value.item())
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            return {
                "encoding": "complex-split",
                "shape": list(value.shape),
                "real": jsonable(value.real),
                "imag": jsonable(value.imag),
            }
        return [jsonable(item) for item in value.tolist()]
    if isinstance(value, pd.DataFrame):
        return {
            "columns": list(value.columns),
            "rows": [jsonable(row) for row in value.to_dict(orient="records")],
        }
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return jsonable(value.model_dump())
    raise TypeError(f"Unsupported result value: {type(value)!r}")
