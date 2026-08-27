# Engineering Learning Platform

A self-hosted interactive engineering-learning system for course folders that combine concise explanations, live controls, MATLAB-class plots, numerical experiments, and short feedback loops.

The platform is intentionally split into:

- **course content**: portable folders under `courses/` or mounted from external repositories;
- **numerical runtimes**: trusted Python experiment functions using NumPy/SciPy/pandas;
- **lesson UI**: a React renderer for controls, predictions, metrics, plots, tables, and explanations;
- **deployment**: one production container and one exposed HTTP port.

The included `demo-radar` course contains an interactive version of **Measure Range from Echo Delay** to prove the full vertical slice. `platform-showcase` exercises WebGL signals, FFTs, I/Q, heatmaps, a 3-D surface, a polar plot, dataframe-style tables, and direct drag manipulation.

## Experience target

Each module follows a compact loop:

1. Read a short concept or physical model.
2. Commit to a prediction.
3. Move a slider, toggle a failure mode, or manipulate a scenario.
4. Watch plots and metrics update immediately.
5. Read an explanation tied to the current state.
6. Complete a focused check before moving on.

A module that has no useful controls can simply declare static plots and narrative blocks.

## Run locally

Prerequisites: Node.js 22+, npm, Python 3.12+, and `uv`.

```bash
npm install
uv sync --project apps/api --extra dev
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` to the FastAPI service on port `8000`.

## Run on one production port

```bash
docker compose up --build
```

Open `http://localhost:8080`.

The production image builds the React site, installs the Python API, serves the compiled site from FastAPI, and exposes only port `8080`.

## Add courses

Place a course folder under `courses/`:

```text
courses/
└── my-course/
    ├── course.yaml
    └── modules/
        └── 01-first-concept/
            ├── module.yaml
            ├── lesson.md
            └── experiment.py
```

The 13 engineering curriculum repositories are pinned as Git submodules under
`courses/`. Clone them with the platform by using:

```bash
git clone --recurse-submodules https://github.com/tranquilWorks/engineering-learning-platform.git
```

For an existing checkout, initialize or refresh them with:

```bash
git submodule update --init --recursive
```

External course roots can be mounted read-only and added with:

```bash
ELP_COURSE_PATHS=/courses:/mounted/controls-course:/mounted/radar-course
```

See [Course authoring](docs/COURSE_AUTHORING.md) and the reusable template under `courses/_template/`.

## Design principles

- Course folders are the canonical curriculum source.
- The web platform owns rendering and execution contracts, not subject-matter content.
- Plotly JSON is the first plotting interchange, allowing line, scatter, heatmap, contour, polar, Smith, 3-D surface, volume, and WebGL traces.
- Small results travel as JSON; Apache Arrow transport is a planned large-data path.
- MATLAB scripts may remain as reference implementations and golden-vector producers, but the learner-facing runtime uses explicit, testable experiment functions.
- Runtime code is trusted build-time content. Arbitrary learner-authored code is not executed.
- Course and module schemas are versioned and validated before deployment.

## Repository map

```text
apps/web/                 React/Vite learner UI
apps/api/                 FastAPI catalog and experiment runtime
courses/                  built-in or mounted course folders
packages/lesson-schema/   portable course/module JSON Schemas
docs/                     architecture, authoring, deployment, roadmap
contracts/                product and active-batch engineering contracts
scripts/                  validation, development, and publish helpers
```

## Verification

```bash
make verify-backend
make validate-courses
npm run typecheck
npm run build
```

`make verify` runs the complete local contract once JavaScript dependencies are installed.

## Portfolio Control

This repository is designed for onboarding to `tranquilWorks/portfolio-control` with the `product-data` profile. Product-specific rules live in `AGENTS.md`; machine-readable requirements and the first bounded batch are in `contracts/`.

The generated Portfolio Control overlay is delivered beside this repository in `engineering-learning-platform-portfolio-control/`.
