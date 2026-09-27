# Current state

`ELP-DSP-FIDELITY-P41-P52` continues issue 441 as one twelve-lesson batch,
from merged PR #47 (`f78831b23e46ff1cb9518a716ac8ba5aeab5a3ee`).
Control PR #508 authorization: `47b907458622f3381bc93e5c19908a487c98774c`.

All twelve source-specific experiments and sixty independent scenario pairs
are implemented. Comparisons passed at 1e-8 absolute/scaled-relative tolerance;
maximum absolute difference is 9.094947017729282e-13. All required local gates
passed: 585 focused DSP tests, 72 contract tests, 965 API tests in each quick/full
run, frontend typecheck/build, lint, catalog, scope and API/live HTTP smoke.
PR #48 is ready for review; protected merge awaits separate owner approval.
Topics span clutter/Swerling, range-Doppler, detection, ROC,
CFAR windows/loss/variants, two-dimensional thresholds, stress and Monte Carlo.

P01 is already distinct; P02-P40 are prior repairs; P41-P52 are current repairs;
P53-P84 remain pending. Source/course identities, source map, conversion manifest,
other courses and platform/UI/workflows remain unchanged. Only twelve coverage
digests change. Inventory remains six courses / 290 modules / 290 interactive.
Whole-course numerical/curriculum/capstone maturity remains blocked.
No MATLAB, browser/accessibility, learner, hardware or production claim.

The full rerun and local preview bound numerical-library threads to one after
three catalog timeouts in unchanged robotics P58; runtime limits were preserved.
Hosted implementation CI had 931 passes and 34 missing-source/history failures;
frontend passed. See the batch evidence for exact results and retained logs.
