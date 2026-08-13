# Architecture

## Purpose

Engineering Learning Platform is a generic, self-hosted renderer and numerical execution service for engineering courses. It gives course authors a professional learning surface without requiring every course to become its own web application.

The central architectural rule is:

> Course repositories own domain truth. The platform owns the lesson contract, rendering primitives, safe execution boundary, and deployment mechanics.

## System context

```text
Browser
  │
  │ HTTP / one exposed port
  ▼
FastAPI application
  ├── serves compiled React UI
  ├── discovers mounted course folders
  ├── validates course/module manifests
  ├── executes trusted experiment entrypoints
  └── serializes Plotly/table/metric results
          │
          ├── built-in courses/
          └── read-only mounted course repositories
```

Development uses two processes for fast iteration:

```text
Vite :5173 ──proxy /api──► FastAPI :8000
```

Production uses one process and one port:

```text
FastAPI :8080
  ├── /api/v1/*
  └── /* compiled React SPA
```

## Frontend

`apps/web` is a React + TypeScript application. It provides:

- course library and module navigation;
- responsive learner layout;
- declarative controls: slider, number, toggle, select, segmented, and action button;
- prediction/reveal blocks;
- live metrics and interpretation callouts;
- Markdown, GitHub-flavored Markdown, and KaTeX equations;
- Plotly figures, including WebGL, heatmap, contour, polar, Smith, ternary, 3-D surface, mesh, cone, streamtube, and volume-compatible traces;
- dataframe-like tables using TanStack Table;
- stale-request cancellation and debounced experiment execution;
- mobile controls and keyboard-accessible native form elements.

The frontend does not contain radar, controls, RF, or other course-specific equations.

## Course catalog

Course roots are configured with the platform path separator:

```bash
ELP_COURSE_PATHS=/app/courses:/mnt/dsp-radar:/mnt/controls-gnc
```

Each root may be either:

1. a single course directory containing `course.yaml`; or
2. a collection directory whose immediate children contain `course.yaml`.

Templates and directories beginning with `_` are ignored.

The catalog is immutable between reloads. Production deployment should treat mounted courses as read-only and rebuild/reload after reviewed changes.

## Native course contract

```text
course-root/
├── course.yaml
├── assets/                         optional
└── modules/
    └── 30-example/
        ├── module.yaml
        ├── lesson.md               optional source blocks
        ├── experiment.py           for trusted Python modules
        ├── assets/                 optional module media
        └── reference/
            └── matlab/             optional golden/reference implementation
```

`module.yaml` declares the controls, ordered lesson blocks, runtime, and source references. The runtime returns a result envelope:

```json
{
  "metrics": [],
  "plots": {},
  "tables": {},
  "explanations": {},
  "warnings": [],
  "diagnostics": {}
}
```

The platform inserts the resolved parameter state into the response.

## Plot interchange

Plotly figure JSON is the version-one interchange:

```python
return {
    "plots": {
        "range_doppler": {
            "data": [
                {
                    "type": "heatmap",
                    "x": ranges_m,
                    "y": velocities_mps,
                    "z": magnitude_db,
                    "colorscale": "Viridis",
                }
            ],
            "layout": {
                "xaxis": {"title": "Range (m)"},
                "yaxis": {"title": "Velocity (m/s)"},
            },
            "config": {"responsive": True}
        }
    }
}
```

This keeps plots portable and decouples the numerical runtime from React. It also maps naturally from Python, MATLAB-exported data, pandas, NumPy, and future remote services.

### Complex values

Complex arrays are not directly JSON-native. A course should expose one or more explicit representations:

- `real` and `imag` columns;
- magnitude and phase;
- an I/Q scatter trace;
- structured objects such as `{ "real": ..., "imag": ... }` for small diagnostic values.

The platform serializer handles NumPy scalars, arrays, pandas Series/DataFrames, and complex scalars. Course authors remain responsible for choosing the representation that teaches the concept.

### Large data

Version one intentionally caps inline JSON results with `ELP_MAX_RESULT_BYTES`. The roadmap adds an artifact endpoint using Apache Arrow IPC or Parquet for large matrices and long captures. Plot downsampling belongs in the runtime so the browser receives a pedagogically useful view rather than millions of unexamined points.

## Numerical runtime

Version one runs trusted repository-controlled `experiment.py:run` functions in the API process under a wall-clock contract. It does **not** accept learner code, uploaded Python, package installation, or shell commands.

The function contract is:

```python
def run(parameters: dict[str, object]) -> dict[str, object]:
    ...
```

Properties expected from production course code:

- deterministic default data unless randomness is the lesson;
- fixed seeds for synthetic noise;
- explicit units;
- bounded memory and compute;
- no network access as part of normal execution;
- no filesystem mutation outside an approved scratch directory;
- no global state that causes one learner's run to affect another.

A thread timeout is not a hostile-code sandbox. The worker-isolation milestone moves execution to disposable subprocesses/containers with CPU, memory, filesystem, and wall-clock limits before untrusted authoring or arbitrary uploads are considered.

## MATLAB relationship

MATLAB remains valuable in three roles:

1. canonical/reference implementation;
2. generator of golden vectors and expected metrics;
3. optional licensed runtime adapter in an approved corporate environment.

The learner-facing platform does not require MATLAB. A migrated module should extract its adjustable parameters and computation contract into a native experiment function while preserving the original `.m` file under `reference/matlab/` or in the source course repository.

A future MATLAB Engine worker may implement the same result envelope. It must be separately licensed, isolated, capacity-controlled, and validated against the Python/native path where both exist.

## State and progress

The foundation release is stateless on the server. Course content is read-only, and module parameters live in the browser session. Planned progress storage is an optional service behind an identity-aware interface. It must not be mixed into course canonical data.

## Deployment and identity

The application can sit behind a corporate reverse proxy or ingress:

```text
User ─► corporate SSO / reverse proxy ─► ELP container :8080
```

The application should consume authenticated identity headers only from a trusted proxy after a dedicated identity milestone. Version one does not implement local passwords.

## Observability

The production roadmap includes:

- structured request and experiment timing logs;
- course/module IDs and result size, but no sensitive parameter payloads by default;
- health/readiness endpoints;
- execution timeout and error counters;
- optional OpenTelemetry traces;
- content revision surfaced in the UI and API.

## Extension boundaries

Planned runtime kinds:

- `static` — prose, media, and precomputed plots;
- `python` — local trusted NumPy/SciPy/pandas execution;
- `remote` — approved HTTP/gRPC compute worker;
- `matlab-engine` — licensed isolated MATLAB execution;
- `wasm` — selected browser-side kernels for very low-latency manipulation.

New runtime kinds must preserve the same output contract rather than introducing runtime-specific frontend code.
