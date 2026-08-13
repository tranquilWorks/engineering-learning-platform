# B000 Foundation Plan

## Goal

Deliver a runnable, professional interactive learning platform on one port, with a complete course discovery → control manipulation → trusted computation → advanced visualization vertical slice.

## Acceptance map

| Capability | Evidence |
|---|---|
| Course discovery | catalog unit test and API catalog smoke |
| Module rendering contract | strict manifest models and template fixtures |
| Live numerical experiment | echo-ranging API/runtime test |
| Deterministic default | double-execution course validator |
| Advanced plotting | platform showcase returns line, WebGL, heatmap, 3-D surface, polar, and table outputs |
| One-port deployment | multi-stage Dockerfile and Compose contract |
| Security baseline | path checks, parameter allow-list, response cap, unprivileged/read-only container configuration |
| Professional frontend | responsive React shell, controls, metrics, Markdown/KaTeX, Plotly, tables, prediction and callout blocks |

## Validation

```bash
PYTHONPATH=apps/api/src python3 scripts/validate_courses.py --execute --deterministic
PYTHONPATH=apps/api/src pytest -q apps/api/tests
npm run typecheck
npm run build
docker compose build
```

Only validations actually executed may be claimed. In an offline environment, unresolved npm/Python dependency installation is an environment gate rather than a passing result.
