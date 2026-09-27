# Numerical replay validation repair — 2026-09-26

Control authorization: merged tranquilWorks/portfolio-control#501,
`1713665398b4d570611e7e8e19195d25fb8b7b38`. The installed active contract is
byte-identical to that merged contract. Clean target entry point:
`01a510244801cbf2c3b7ce990693aac9dc5959c1`, tree
`a757015ceca672e34d0d73bc94d6527cf5c6f0fb`.

## Problem and repair

The unchanged baseline produced 671 passing tests and 14 failures under Python
3.12.13 / NumPy 2.5.3 / SciPy 1.18.1. Exact historical floating-point replay and
comparison of current error extrema with saved historical extrema caused the
failures. `ELP-VERIFY-REPLAY-01-baseline-failures.txt` records every failure. Default BLAS threading
and a separate NumPy 2.5.2 probe did not resolve this portability issue.

The test-only comparator checks every finite real signature component against:

`min(1e-9 * max(1, abs(saved)), 0.01 * max(scientific_atol, scientific_rtol * abs(saved)))`.

Both independently recomputed reference and production signatures must replay
saved evidence under that stricter limit. Fresh production/reference comparisons
still pass the original scientific checks. GNC P01-P24 recorded metrics are
recomputed from the immutable saved pair; current error extrema are evaluated
separately. No fixture, scientific tolerance, course algorithm or oracle changed.

The DSP regression now verifies the exact completed P11-P20 contract retained
from baseline. Snapshot SHA-256:
`a834748236ec70a0728322aa10340aad9f6f498a516fba8e2c1dda82f687f4ea`;
baseline Git blob: `d4282cef4b773182e434ec5af6725ea8af207277`.
The snapshot keeps historical source and scope checks independent of which batch
is active, without requiring a deep Git checkout.

## Read-only audit and negative controls

The retained audit script recomputes 780 scenarios and compares 1,560 saved/live
reference and production signatures. It never writes course fixtures. Detailed
rows are retained in `ELP-VERIFY-REPLAY-01-audit.json`: zero failures, worst
budget use 0.11726841719905677 (11.73%). The preliminary reference
audit found largest scaled drift `1.1726841719905678e-10` at GNC P18; outside
that case, the maximum was `9.094947017729282e-13` at Vehicle P34.

Negative tests reject material drift within a loose scientific tolerance, a
large unrelated component hiding a small-component error, wrong order/shape/
length, empty vectors, NaN/Inf, strings/booleans/complex numbers, invalid
tolerances and corrupted historical metrics. A separate counterexample passes
replay yet fails scientific acceptance. Zero tolerance still requires equality.

## Verification

All required local gates passed. Exact commands are in `contracts/verification.yaml`.

| Gate | Result |
| --- | --- |
| Affected replay/course regression | 178 passed; final helper suite separately confirms the added mixed-boolean case |
| Final replay negative/positive controls | 40 passed |
| DSP source-attested regression | 345 passed |
| Contract wrapper | 72 passed |
| Quick wrapper | 725 passed, 3 existing dependency deprecation warnings |
| Full wrapper / `scripts/verify.sh` | 725 passed, schema export/current schemas, deterministic catalog, frontend typecheck and production build passed |
| Standalone deterministic catalog JSON | 6 courses, 290 modules, 290 interactive, no errors |
| Changed Python test lint | Passed; obsolete UP038 ignore produces only an informational warning |
| Scope/source immutability and whitespace | Passed; every change is allowed, forbidden paths have no diff from baseline |

The full build retains its existing large Plotly chunk warning. The three Python
warnings concern Starlette/httpx and FastAPI ORJSONResponse deprecations; no
runtime/dependency behavior was changed in this test-only batch. Test and build
logs use the `ELP-VERIFY-REPLAY-01-replay-*` prefix. Retained text logs remove
terminal color codes and trailing whitespace; numerical values and results are unchanged. Python environment versions
are retained separately; frontend used Node 22.23.3. This is software verification
only, not browser/accessibility or deployment evidence.

## Control verification and hosted limitation

Before activation, the exact control PR head passed `validate-control-plane.sh`:
252 root tests (one unrelated uninitialized-GitG skip), 33 ELP tests, six
analog-camera tests, 15 Tranquility tests, portfolio validation and shellcheck.
Hosted control run 36277641475/job 108503347075 executed no steps: GitHub reported
failed recent account payments or a spending limit requiring adjustment.
The normal merge succeeded under existing owner authorization; no access-control
bypass was used. Hosted CI is reported separately from mandatory local gates.

## Boundaries and next step

Six courses, 290 modules, 290 interactive modules; issue 441 remains open.
P21-P84 is pending. Rebind P21-P28 to the exact merged repair baseline before
activation. Target merge retains human approval. No MATLAB, audio, browser/
accessibility, learner, hardware, release/deployment or production claim.

Rollback: revert this test-only repair and activation overlay. No data migration,
course artifact change or learner-state change occurs.
