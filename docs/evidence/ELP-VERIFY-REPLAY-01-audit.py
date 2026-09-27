import importlib.util
import json
from pathlib import Path

import numpy as np
from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

root = Path("courses")
catalog = CourseCatalog([root])
runtime = ExperimentRuntime(catalog)
rows = []
for course in ["controls-gnc", "robotics-autonomy", "vehicle-dynamics"]:
    for filename in ["reference_cases.py", "expansion_reference_cases.py"]:
        if filename == "reference_cases.py" and course != "controls-gnc":
            continue
        spec = importlib.util.spec_from_file_location(
            "audit_reference", root / course / filename
        )
        ref = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ref)
        for folder in sorted((root / course / "modules").iterdir()):
            n = int(folder.name[:2])
            if (filename == "reference_cases.py") != (n <= 24):
                continue
            fixture = folder / "evidence/expected-independent.json"
            if not fixture.exists():
                continue
            import yaml

            tol = (
                ref.tolerance(n)
                if filename == "reference_cases.py"
                else yaml.safe_load((folder / "design.yaml").read_text())["tolerance"]
            )
            expected = json.loads(fixture.read_text())
            actual = json.loads(
                (folder / "evidence/actual-production.json").read_text()
            )
            for scenario, case in expected["cases"].items():
                reference = np.array(
                    ref.reference_signature(n, case["parameters"]), float
                )
                production = np.array(
                    runtime.run(course, folder.name, case["parameters"]).diagnostics[
                        "signature"
                    ],
                    float,
                )
                for label, live, saved in [
                    ("reference", reference, np.array(case["signature"], float)),
                    (
                        "production",
                        production,
                        np.array(actual["cases"][scenario]["signature"], float),
                    ),
                ]:
                    budget = np.minimum(
                        1e-9 * np.maximum(1, abs(saved)),
                        0.01
                        * np.maximum(tol["absolute"], tol["relative"] * abs(saved)),
                    )
                    delta = abs(live - saved)
                    rows.append(
                        {
                            "course": course,
                            "item": n,
                            "scenario": scenario,
                            "kind": label,
                            "max_budget_fraction": float(
                                np.max(
                                    np.divide(
                                        delta,
                                        budget,
                                        out=np.zeros_like(delta),
                                        where=budget != 0,
                                    )
                                )
                            ),
                            "passed": bool(np.all(delta <= budget)),
                        }
                    )
print(
    json.dumps(
        {
            "rows": rows,
            "comparisons": len(rows),
            "failures": [r for r in rows if not r["passed"]],
            "largest": sorted(
                rows, key=lambda r: r["max_budget_fraction"], reverse=True
            )[:12],
        },
        indent=2,
    )
)
