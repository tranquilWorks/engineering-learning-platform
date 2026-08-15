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
        if not math.isfinite(value):
            raise ValueError("non-finite floating-point values are not valid results")
        return value
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
        if not all(isinstance(key, str) for key in value):
            raise TypeError("result mappings require string keys")
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, set):
        raise TypeError("unordered sets are not valid deterministic results")
    if hasattr(value, "model_dump"):
        return jsonable(value.model_dump())
    raise TypeError(f"Unsupported result value: {type(value)!r}")
