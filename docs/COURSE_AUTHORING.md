# Course Authoring

## Authoring goal

A module is not a script with sliders bolted on. It is a short learning loop:

```text
concept → prediction → manipulation → evidence → explanation → check → bridge
```

Use controls only when changing them reveals a meaningful cause/effect relationship. A static module with excellent plots is better than an interactive module with arbitrary knobs.

## Start a course

Copy `courses/_template` or mount an independent course repository.

```text
my-course/
├── course.yaml
└── modules/
    └── 01-first-module/
        ├── module.yaml
        ├── lesson.md
        └── experiment.py
```

### `course.yaml`

```yaml
schema_version: 1
id: controls-gnc
title: Controls and GNC
order: 20
description: Interactive dynamics, estimation, and control experiments.
modules_path: modules
tags: [controls, estimation, guidance]
```

IDs are stable machine identifiers. Do not rename them to improve display copy; change `title` instead.

## Define a module

```yaml
schema_version: 1
id: 03-second-order-response
number: 3
title: See Damping Change a Transient
summary: Connect damping ratio to overshoot and settling time.
guiding_question: What does damping change in a second-order system?
status: implemented
runtime:
  kind: python
  entrypoint: experiment.py:run
  trust: local-trusted
  timeout_seconds: 3
controls:
  - id: zeta
    type: slider
    label: Damping ratio
    default: 0.45
    minimum: 0.05
    maximum: 1.5
    step: 0.01
blocks:
  - type: markdown
    source: lesson.md
  - type: prediction
    text: What happens to overshoot as ζ approaches one?
    reveal: Overshoot falls to zero at critical damping, while rise behavior also changes.
  - type: controls
  - type: metrics
  - type: plot
    title: Step response
    plot: step_response
  - type: callout
    source: interpretation
    tone: info
```

## Controls

Supported control types:

| Type | Use |
|---|---|
| `slider` | Continuous or finely stepped scalar exploration |
| `number` | Exact numeric entry where a slider would be awkward |
| `toggle` | Enable a target, failure, correction, model term, or comparison |
| `select` | Choose among many named modes or algorithms |
| `segmented` | Choose among a few prominent alternatives |
| `button` | Trigger a deterministic regenerate/reset/action event |

A numeric control requires `minimum` and `maximum`. Add `step`, `unit`, and `description` whenever they clarify interpretation.

Conditional display uses exact parameter matching:

```yaml
visible_when:
  second_target: true
```

Keep controls few enough that a learner can form a hypothesis. Advanced modules may group controls in a future schema revision; version one uses one ordered list.

## Lesson blocks

| Block | Purpose |
|---|---|
| `markdown` | Narrative and equations from a source file or inline text |
| `prediction` | Prompt plus an intentionally hidden reveal |
| `controls` | Mobile placement for declared controls; desktop controls stay sticky |
| `metrics` | All current metrics from the runtime |
| `plot` | One named Plotly figure |
| `plot_grid` | Linked peer plots |
| `table` | Dataframe-like table |
| `callout` | Static text or dynamic `explanations[source]` |
| `widget` | Allow-listed direct-manipulation component, configured through `widget` and `props` |
| `divider` | Visual transition |

Blocks are rendered in declared order. The course determines the pedagogy; the platform does not reorder it.

## Experiment contract

```python
from typing import Any


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    # validate assumptions close to the computation
    value = float(parameters["value"])

    return {
        "metrics": [
            {
                "id": "result",
                "label": "Result",
                "value": value**2,
                "unit": "m²",
                "emphasis": "primary",
            }
        ],
        "plots": {
            "main": {
                "data": [{"type": "scatter", "x": [0, 1], "y": [0, value]}],
                "layout": {
                    "xaxis": {"title": "Time (s)"},
                    "yaxis": {"title": "Position (m)"},
                },
            }
        },
        "tables": {},
        "explanations": {
            "interpretation": "This text may depend on the current state."
        },
        "warnings": [],
        "diagnostics": {},
    }
```

### Metrics

Metric values should be scalar and unit-bearing when applicable. Emphasis options are `normal`, `primary`, `warning`, and `danger`. Do not use `danger` merely for visual variety.

### Plotly

Return Plotly-compatible `data`, `layout`, and `config`. Useful engineering trace types include:

- `scatter` / `scattergl` for sampled signals and long traces;
- `heatmap` for spectrograms, confusion matrices, covariance, and range–Doppler maps;
- `contour` for level sets and objective landscapes;
- `surface`, `mesh3d`, and `volume` for higher-dimensional fields;
- `scatterpolar` and `barpolar` for antenna patterns and angular data;
- `scattersmith` for RF reflection data;
- `cone` and `streamtube` for vector fields.

Always label axes and units. Use `uirevision: keep-view` when a live update should preserve the learner's zoom/camera.

### Tables and pandas

The serializer accepts pandas DataFrames directly, but the explicit transport contract is:

```python
{
    "tables": {
        "results": {
            "columns": ["case", "rmse", "bias"],
            "rows": dataframe[["case", "rmse", "bias"]].to_dict(orient="records"),
        }
    }
}
```

Limit rows to what a learner can inspect. Use future Arrow artifacts for large frames.

## Static plots

A static lesson may use:

```yaml
runtime:
  kind: static
```

Version one supports prose directly. Precomputed plot assets are on the roadmap; until then, use a trivial trusted experiment if a static lesson needs Plotly JSON.

## Migrating a MATLAB-first module

Do not translate line-by-line. Use this sequence:

1. **Freeze the MATLAB baseline.** Record input parameters, figure inventory, expected metrics, seed, MATLAB version, and toolboxes.
2. **Identify the learning variables.** Separate parameters that reveal the concept from internal numerical settings.
3. **Extract a calculation contract.** Define parameter names, units, output metrics, plot datasets, tables, and interpretation text.
4. **Preserve the reference.** Keep the `.m` file and representative output/golden vectors under `reference/matlab/` or in the source repository.
5. **Implement the native experiment.** Prefer NumPy/SciPy/pandas, explicit operations, and deterministic data.
6. **Compare numerically.** Test selected vectors against MATLAB tolerances. Do not claim equivalence from visual similarity.
7. **Design the lesson loop.** Prediction first, smallest useful control set, one failure mode, and a bridge to the next concept.
8. **Validate the module.** Run course validation, deterministic execution, UI review, and accessibility review.

### Suggested media-targeted second pass

When revising existing course modules for this platform, add:

- `module.yaml` with controls and ordered blocks;
- `experiment.py` or approved adapter;
- concise `lesson.md` sections rather than a long script walkthrough;
- plot keys that remain stable across parameter changes;
- `reference/matlab/` notes and golden vectors;
- optional images/video under `assets/` with captions and alt text;
- a migration evidence note specifying what is equivalent, approximate, or not yet implemented.

## Validation

```bash
make validate-courses
make verify-backend
npm run typecheck
npm run build
```

For a mounted course repository:

```bash
ELP_COURSE_PATHS=/path/to/my-course \
  PYTHONPATH=apps/api/src \
  python3 scripts/validate_courses.py --execute --deterministic
```

## Module media

Put module-owned images and downloadable media under `assets/`. Relative Markdown image paths such as `assets/range-geometry.svg` are rewritten to the protected module asset endpoint. Dotfiles and paths escaping the asset directory are rejected.

## Widget example

```yaml
- type: widget
  title: Drag the operating point
  widget: parameter-map
  props:
    x_control: frequency_hz
    y_control: snr_db
    x_label: Frequency (Hz)
    y_label: SNR (dB)
```

Only platform-registered widget IDs render. Independent course folders cannot ship executable frontend JavaScript.
