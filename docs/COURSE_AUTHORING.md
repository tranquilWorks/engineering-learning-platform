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

`schema_version` is required and must be the integer `1`; booleans, strings,
missing values, older values, and future values are rejected. Unknown fields
are errors rather than extension points. Propose a generic platform-contract
change before authoring a new control, block, widget, runtime, or envelope field.

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

## DSP/Radar item conversion

The DSP/Radar course uses a governed, one-item conversion lane rather than a
bulk importer. Its canonical source is the read-only
`courses/dsp-radar-learning` gitlink at
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`; its platform-owned native course
is `courses/dsp-radar`. The complete normative procedure is in
`courses/dsp-radar/AUTHORING.md`.

ELP-DSP-00 creates only the source map, conversion manifest, coverage ledger,
closed conversion schema, and an empty native course. It starts at 84 pending
and zero converted items. It does not create a learner module, copy MATLAB, or
claim that any of the 84 lessons is visible or Pythonized.

Successor batches run in this fixed order:

```text
ELP-DSP-P01 -> ELP-DSP-P02 -> ... -> ELP-DSP-P84
```

Each batch creates exactly one mapped module and may advance only that item from
`pending` to `converted`. A blocked item stops the ordered lane. Do not create
empty manifests, TODO lessons, copied-source shells, or other placeholders to
make catalog coverage appear complete.

For one item, preserve the source identity and precedence:

1. `README.md` fixes the experiment, goal, and completion condition.
2. `lesson.md` fixes the concept, physical model, equations, limiting cases,
   and common mistakes.
3. `walkthrough.md` fixes the learner sequence, expected observations, two or
   more useful sweeps, broken case, and recovery.
4. `checks.md` fixes observation, prediction, interpretation, and teach-back
   checks.
5. `experiment.m` fixes constants, deterministic data, operations, important
   plot order and labels, assertions, and resource guards.

Canonical source identity remains uppercase `P##`. The lowercase native module
ID is the basename of the target folder recorded in the immutable conversion
manifest. The native manifest must retain the same module number, title,
guiding question, and curriculum order.

A converted module is a complete native lesson, not merely a catalog row. It
requires an exact-v1 `module.yaml`, a concise learner-facing `lesson.md`, a
self-contained bounded `experiment.py`, and a closed `conversion.yaml`. Its
lesson blocks must implement the concept-to-prediction-to-manipulation loop,
stable result references, labeled controls, unit-bearing plots, immediate
interpretation, two useful one-variable sweeps, one intentional failure and
recovery, common mistakes, and a completion/teach-back check.

The Python entrypoint must be self-contained because current revision identity
binds the direct entrypoint but not undeclared imported helpers. It must use
fixed seeds where applicable, reject invalid or excessive inputs before
allocation, declare resource bounds, return finite deterministic values, and
keep its default run suitable for catalog promotion.

`conversion.yaml` must record passing named Python/source-equivalence cases
with exact inputs, units, expected and actual identities, tolerances, measured
errors, and commands. This is independent numerical evidence derived from the
pinned source contract; it is not proof that MATLAB ran. MATLAB runtime parity
is reported separately as `passed`, `failed`, or `not_run`, and `passed`
requires retained evidence from an actual identified MATLAB runtime.

Use precise readiness language:

- **mapped**: present in the immutable 84-item inventory;
- **catalog-visible**: a real native module manifest exists;
- **converted**: the complete Python lesson and required equivalence evidence
  pass;
- **browser-reviewed** or **accessibility-reviewed**: the named manual review
  actually occurred; and
- **MATLAB-parity passed**: the recorded MATLAB comparison actually ran.

None of these states implies the next. The final aggregate Python gate reviews
all 84 converted items, browser/accessibility results, residual numerical
differences, and every explicit MATLAB `not_run` or `failed` record.

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

## Revision identity

Catalog and module API documents expose the exact schema version, deterministic
content SHA-256, and source Git commit when available. Non-Git mounts explicitly
report no Git revision. Experiment requests include the displayed module digest;
the API rejects stale requests after a catalog reload. Results repeat course and
module identities and add platform/runtime identities so evidence can bind the
exact pair that ran.

Validation and generation are read-only with respect to course roots. Generate
all JSON Schema and TypeScript derivatives together with:

```bash
PYTHONPATH=apps/api/src python3 scripts/export_schemas.py
PYTHONPATH=apps/api/src python3 scripts/export_schemas.py --check
```

The generated derivatives describe only the current executable contract and do
not promise historical compatibility. Recovery is a reviewed Git pin or revert
of the platform and course to their last validated pair.
