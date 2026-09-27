# Current state

`ELP-DSP-FIDELITY-P29-P40` continues issue 441 as a twelve-lesson batch requested
by the owner, from merged PR #46 (`74fbe13828665783a97d047eae0c6dc6ef482745`).
Control authorization is `a4b075fe1e4fdb35d58802668d2631b9f465eba3`.

All twelve source-specific experiments and sixty independent scenario pairs
are implemented. Numerical comparisons passed at a declared 1e-8 tolerance;
all required local verification passed at implementation revision
`3c5cee0dc8bef78f9f3c8baed691f03c4023d804`: 495 focused DSP tests,
72 contract tests, all 875 API tests in both quick and full wrappers,
frontend typecheck/build, deterministic catalog, lint and service/scope checks.
PR #47 is ready for review; protected merge awaits separate owner approval.
Hosted backend CI has 22 missing-source/history failures; frontend passed.
The group spans power budgets, ranging, pulse compression, ambiguity, Doppler,
MTI, blind speeds and coherent/noncoherent integration.

P01 is already distinct; P02-P28 are prior repairs; P29-P40 are current repairs;
P41-P84 remain pending. Source/course identities, source map, conversion manifest,
other courses, platform/UI and workflows remain unchanged. Only twelve coverage
digests change. Inventory stays six courses / 290 modules / 290 interactive.
Whole-course numerical/curriculum/capstone maturity remains blocked.

No MATLAB runtime, browser/accessibility, learner, hardware, certification,
release/deployment or production validation is claimed.
