"""Bind individually authored prompts to actual controls and curriculum identities."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "courses/vehicle-dynamics"


def write_manifest(path, module):
    # Previously reviewed source manifests are JSON; scoped verifiers consume JSON.
    if path.read_text().lstrip().startswith("{"):
        path.write_text(json.dumps(module, indent=2) + "\n")
    else:
        path.write_text(yaml.safe_dump(module, sort_keys=False, width=100))


def main():
    curriculum = yaml.safe_load((COURSE / "competency-map.yaml").read_text())
    prompts = json.loads((COURSE / "assessment-prompts.json").read_text())
    lessons = []
    for prompt in prompts:
        n = prompt["number"]
        folder = next((COURSE / "modules").glob(f"{n:02d}-*"))
        path = folder / "module.yaml"
        module = yaml.safe_load(path.read_text())
        record = yaml.safe_load(
            (folder / ("verification.yaml" if n <= 24 else "design.yaml")).read_text()
        )
        equations = (
            [record["governing_relation"]] if n <= 24 else record["governing_equations"]
        )
        scenarios = (
            {r["name"]: r["inputs"] for r in record["scenarios"]}
            if n <= 24
            else record["scenarios"]
        )
        baseline = scenarios["baseline"]
        lines = []
        for scenario in ["sweep_1", "sweep_2"]:
            differences = [
                f"`{k}`: {baseline[k]} → {v}"
                for k, v in scenarios[scenario].items()
                if baseline[k] != v
            ]
            lines.append(
                "- "
                + "; ".join(differences)
                + ". Hold the other controls at baseline; predict and explain the change before executing."
            )
        memberships = [
            c["id"]
            for c in curriculum["competencies"]
            if f"P{n:02d}" in c["module_ids"]
        ]
        assert memberships
        row = {
            **prompt,
            "id": f"VD-F{n:02d}",
            "module_id": module["id"],
            "competency_ids": memberships,
            "assessment_file": str((folder / "assessment.md").relative_to(COURSE)),
            "plot_keys": [
                key
                for b in module["blocks"]
                if b["type"] == "plot_grid"
                for key in b["plots"]
            ],
            "learner_result": "not_recorded",
        }
        lessons.append(row)
        text = (
            f"""# P{n:02d} course checkpoint

## Predict and derive

{prompt["task"]}

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

"""
            + "\n".join("- `" + e + "`" for e in equations)
            + """

## Controlled comparison

"""
            + "\n".join(lines)
            + f"""

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

{prompt["expected_reasoning"]}

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

{prompt["claim_limit"]}

Competency links: {", ".join(memberships)}. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
"""
        )
        previous = folder / "prior-assessment.md"
        if (
            (folder / "assessment.md").exists()
            and not previous.exists()
            and not (COURSE / "assessment-map.json").exists()
        ):
            previous.write_bytes((folder / "assessment.md").read_bytes())
        if previous.exists():
            text += "\n\n# Retained scoped evidence task\n\n" + previous.read_text()
        (folder / "assessment.md").write_text(text)
        if not any(b.get("source") == "assessment.md" for b in module["blocks"]):
            module["blocks"].append(
                {
                    "type": "markdown",
                    "title": "Course checkpoint",
                    "source": "assessment.md",
                }
            )
        write_manifest(path, module)
    # Rebuild only generated portfolio bindings, removing obsolete anchors.
    for folder in (COURSE / "modules").iterdir():
        for old in folder.glob("portfolio-a-*.md"):
            old.unlink()
        path = folder / "module.yaml"
        if path.exists():
            module = yaml.safe_load(path.read_text())
            module["blocks"] = [
                b
                for b in module["blocks"]
                if not b.get("source", "").startswith("portfolio-a-")
            ]
            write_manifest(path, module)
    portfolio_prompts = json.loads((COURSE / "portfolio-prompts.json").read_text())
    portfolios = []
    for a in curriculum["assessments"]:
        if not a["id"].startswith("A-"):
            continue
        numbers = sorted(
            {
                int(m[1:])
                for c in curriculum["competencies"]
                if c["id"] in a["competency_ids"]
                for m in c["module_ids"]
            }
        )
        if a["id"] == "A-CAP-TELEMETRY":
            numbers = [n for n in numbers if n != 67]
            anchor = 66
        elif a["id"] == "A-CAP-DIGITAL":
            numbers = [n for n in numbers if n != 66]
            anchor = 67
        else:
            anchor = max(numbers)
        folder = next((COURSE / "modules").glob(f"{anchor:02d}-*"))
        title = "Cumulative portfolio " + a["id"]
        candidates = [r for r in lessons if r["number"] in numbers]
        # Four different authored prompts anchor the cumulative cross-module tasks.
        selected = [
            candidates[0],
            candidates[len(candidates) // 3],
            candidates[2 * len(candidates) // 3],
            candidates[-1],
        ]
        body = (
            f"# {a['id']} integration evidence\n\nIntegrate these existing lessons: "
            + ", ".join(f"P{n:02d}" for n in numbers)
            + ".\n\nRequired evidence: "
            + a["evidence"]
            + "\n\n"
        )
        labels = [
            "Derive and predict",
            "Compare connected mechanisms",
            "Diagnose and recover",
            "Integrate and defend the boundary",
        ]
        for label, prompt in zip(labels, selected):
            body += f"## {label}\n\nUse P{prompt['number']:02d}: {prompt['task']} {prompt['expected_reasoning']} Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.\n\n"
        body += (
            "## Required integration artifact\n\n" + portfolio_prompts[a["id"]] + "\n\n"
        )
        body += """## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
"""
        filename = "portfolio-" + a["id"].lower() + ".md"
        (folder / filename).write_text(body)
        p = folder / "module.yaml"
        m = yaml.safe_load(p.read_text())
        m["blocks"] = [b for b in m["blocks"] if b.get("source") != filename] + [
            {"type": "markdown", "title": title, "source": filename}
        ]
        write_manifest(p, m)
        portfolios.append(
            {
                **a,
                "anchor_number": anchor,
                "module_ids": [r["module_id"] for r in candidates],
                "assessment_file": str((folder / filename).relative_to(COURSE)),
                "learner_result": "not_recorded",
            }
        )
    curriculum["assessments"] = [
        a for a in curriculum["assessments"] if not a["id"].startswith("VD-F")
    ]
    curriculum["assessments"] += [
        {
            "id": r["id"],
            "type": "formative",
            "competency_ids": r["competency_ids"],
            "evidence": r["task"],
        }
        for r in lessons
    ]
    # Keep the original JSON representation consumed by existing curriculum gates.
    (COURSE / "competency-map.yaml").write_text(json.dumps(curriculum, indent=2) + "\n")
    registry = {
        "schema_version": 1,
        "course_id": "vehicle-dynamics",
        "baseline": "9c27f567399cf2fcb9728fb104b2d573fcac5652",
        "formative_count": len(lessons),
        "cumulative_count": len(portfolios),
        "lessons": lessons,
        "portfolios": portfolios,
    }
    (COURSE / "assessment-map.json").write_text(json.dumps(registry, indent=2) + "\n")
    print(
        f"Bound {len(lessons)} distinct checkpoints and {len(portfolios)} existing curriculum portfolios"
    )


if __name__ == "__main__":
    main()
