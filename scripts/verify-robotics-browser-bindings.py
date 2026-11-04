"""Reconcile complete browser coverage with explicit rechecks of changed plots."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/course-quality"
COURSE = ROOT / "courses/robotics-autonomy"


def reconcile():
    files = [FOLDER / "robotics-aggregate-browser-final.json"] + [
        FOLDER / f"robotics-aggregate-browser-polished-{n}.json"
        for n in [51, 62, 68, 69]
    ]
    rows = {}
    interactions = {}
    sources = []
    screenshots = []
    for file in files:
        report = json.loads(file.read_text())
        assert report["browser_version"] == "141.0.7390.37"
        assert (
            report["manual_screen_reader"]
            == report["representative_learners"]
            == "not_run"
        )
        sources.append(
            {
                "path": str(file.relative_to(ROOT)),
                "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
                "base_url": report["base"],
                "rows": len(report["rows"]),
            }
        )
        for row in report["rows"]:
            assert (
                row["status"] == "passed"
                and row["checkpoint"]
                and row["checkpoint_in_viewport"]
            )
            assert not row["violations"] and not row["errors"]
            assert not row.get("runtime_errors", [])
            assert (
                not row["horizontal_overflow"]
                and not row["math_errors"]
                and not row["plot_errors"]
            )
            assert not row["unsupported_webgl"]
            key = (row["module"], row["viewport"])
            rows[key] = {
                **row,
                "evidence_source": str(file.relative_to(ROOT)),
                "base_url": report["base"],
            }
        for row in report["interactions"]:
            assert (
                row["reset"]
                and row["control_changed"]
                and row["failure_recovery"] == "passed"
            )
            assert (
                not row["post_interaction_plot_errors"] and not row["unsupported_webgl"]
            )
            interactions[(row["module"], row["viewport"])] = {
                **row,
                "evidence_source": str(file.relative_to(ROOT)),
            }
        for shot in report["screenshots"]:
            if file == files[0] and "robotics-integration-" in shot["path"]:
                continue
            screenshots.append({**shot, "evidence_source": str(file.relative_to(ROOT))})
    registry = json.loads((COURSE / "assessment-map.json").read_text())
    expected = {
        (r["module_id"], viewport)
        for r in registry["lessons"]
        for viewport in ["desktop", "mobile"]
    }
    assert set(rows) == set(interactions) == expected and len(rows) == 138
    catalog = CourseCatalog([COURSE])
    for (module, _), row in rows.items():
        _, record = catalog.module_record("robotics-autonomy", module)
        assert row["content_digest"] == record.revision.content_digest, (
            module,
            "stale browser evidence",
        )
    assert sum(len(r["robotics_portfolios"]) for r in rows.values()) == 26
    result = {
        "batch": "ELP-ROB-AGGREGATE-QUALITY-01",
        "status": "passed",
        "validation_level": "automated_chromium_current_input_bindings",
        "browser_version": "141.0.7390.37",
        "source_reports": sources,
        "rows": list(rows.values()),
        "interactions": list(interactions.values()),
        "portfolio_visits": 26,
        "manual_screen_reader": "not_run",
        "representative_learners": "not_run",
        "concurrent_capacity_claimed": False,
        "screenshots": screenshots,
    }
    (FOLDER / "robotics-aggregate-browser-current.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print("138 current-content views/interactions and 26 portfolio visits passed")


if __name__ == "__main__":
    reconcile()
