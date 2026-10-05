# Revision closeout and review handoff — 2026-10-01

Vehicle P13–P16 now have corrected physical models, dimensioned plots, substantial individual lessons and browser-embedded Course checkpoints. This completes all sixteen findings in the owner-authorized twelve-plus-four Vehicle revision under ELP-VEHICLE-DRIVELINE-QUALITY-04. The exact baseline is target PR59 merge `1a0041bd24de1168c03ff2bf2a656a6061cac0e3`; control contract PR584 merged at `24be9b00abf25b29b861241ef0e3204948ea9078` before activation. The implementation is merged in [PR60](https://github.com/tranquilWorks/engineering-learning-platform/pull/60) at `f58533582a617cf48741aa5349f26f5954e21d95`; [Portfolio Control PR588](https://github.com/tranquilWorks/portfolio-control/pull/588) closes it at `4fa6f144c2b2358308889232468ac88e0b27298a`. Both merge trees match their reviewed commits.

Twenty independent local and twenty baked HTTP full-mechanism comparisons passed at unchanged 1e-10 absolute/relative tolerance. The 106 focused/regression tests include all 32 new runtime corners and preserved foundation physics. Twenty-nine closure and active-contract regressions passed. Final delivery passed 290 HTTP modules, 580 desktop/mobile pages, 288 checkpoint checks, twenty cumulative DSP checks, 174 real control/fault/recovery/reset sequences, 176 screenshots, 72 SVG text/legend layout checks and all 290 host/baked identities. Thirteen web tests and 23 focused browser tests passed, including actual-control crossover/redline/unavailable classifications. Eight plot captures were visually inspected. Mandatory gates passed sequentially (contract: 103 tests in 116.81 seconds; quick: 1612 tests in 1657.60 seconds; full: 1612 tests in 1594.55 seconds). See [batch evidence](evidence/ELP-VEHICLE-DRIVELINE-QUALITY-04-2026-09-30.md) and [exact verification summary](course-quality/vehicle-driveline-verification-summary.json).

**Zero named findings remain: Controls 0, Robotics 0, Vehicle 0.** All three non-DSP aggregate numerical, curriculum and capstone reassessments remain blocked; the targeted register is not exhaustive course acceptance. DSP retains its separate authored/software aggregate disposition. The agreed repair batches are complete and published. Course-level numerical, curriculum and capstone acceptance remains a separate review; it may identify further work. Inventory remains 288 engineering lessons plus two examples, with nine pinned source-only repositories.

Verified read-only nonroot development preview: `http://127.0.0.1:8777`; image `sha256:a1e97af00da778bbb271e557d6dae6c3355c43c7f19867224cd78299da644985`. Earlier final previews remain preserved. Hosted CI is separately reported and nonmandatory under owner direction; required local gates passed. Representative learners, manual screen-reader, MATLAB, measured vehicle, hardware, concurrent capacity and production validation remain unperformed.


The owner reconfirmed on 2026-10-01 that CI/CD does not block this development closeout. Hosted PR60 finished with frontend passed, backend failed and container skipped; the control hosted job did not start because of its recorded account restriction. These hosted outcomes remain separate from the successful mandatory local verification. No workflow or protection was changed.

---

<!-- Historical snapshots below retain the status at their recorded dates. -->
# Verified Vehicle foundations revision — 2026-09-30

Vehicle P01–P12 now have corrected physical models and dimensioned plots, twelve substantial individual lessons and twelve browser-embedded Course checkpoints. This completes the first group of the owner-authorized twelve-plus-four Vehicle revision under ELP-VEHICLE-FOUNDATIONS-QUALITY-12. The exact baseline is target PR58 merge `607c716993be14e7b782897ab054a7f8478f5dc0`; control contract PR580 merged at `604c55bfa992cbdb6884f8257cb052cf4b1c7714` before activation. The development PR records integration; Portfolio Control closeout binds the final merge SHA.

Sixty independent local and sixty baked HTTP full-mechanism comparisons passed at 1e-10 absolute/relative tolerance. The 138 expanded regression tests include all 96 Vehicle runtime corners under the unchanged three-second limit, direct physical identities and preserved Robotics checks. Twenty-six closure regressions and three active-contract binding tests also passed. Final delivery passed 290 HTTP modules, 580 desktop/mobile pages, 280 checkpoint checks, twenty cumulative DSP checks, 166 real control/fault/recovery/reset sequences, 168 screenshots, 64 SVG text/legend layout checks and all 290 host/baked content identities. Twenty-two focused browser tests passed, and fifteen plot captures were visually inspected. Mandatory gates passed sequentially (contract: 103 tests in 104.59 seconds; quick: 1583 tests in 1659.85 seconds; full: 1583 tests in 1601.97 seconds). See [batch evidence](evidence/ELP-VEHICLE-FOUNDATIONS-QUALITY-12-2026-09-30.md) and [exact verification summary](course-quality/vehicle-foundations-verification-summary.json).

**Four named findings remain: Controls 0, Robotics 0, Vehicle 4 (P13–P16).** All three non-DSP aggregate numerical, curriculum and capstone reassessments remain blocked; zero named findings does not establish aggregate acceptance. DSP retains its separate authored/software aggregate disposition. Complete this group's normal verified development merge and Portfolio Control closeout, then continue the already-authorized final four against a fresh exact-baseline contract. Inventory remains 288 engineering lessons plus two examples, with nine pinned source-only repositories.

Verified read-only nonroot development preview: `http://127.0.0.1:8776`; image `sha256:d844a5f9ed5ac979dda6e361a713caaa54aea3780210cfc5d8d47c6683b73d18`. Earlier final previews remain preserved. Hosted CI is separately reported and nonmandatory under owner direction; required local gates passed. Representative learners, manual screen-reader, MATLAB, measured vehicle, hardware, concurrent capacity and production validation remain unperformed.

---

# Verified completion of the twenty named Robotics findings — 2026-09-30

The remaining eight Robotics P42-P48/P52 repairs passed under ELP-ROBOTICS-PERCEPTION-QUALITY-08, following the twelve P30-P41 repairs in target PR57 at `f04472f16fc1da00e817d385eaef0a63f3c71b48`. The exact-baseline successor control contract merged at `c26b23f11e8d4dda9d7691b1758f50a227255757` before activation. All twenty requested lessons now contain executed mechanisms, separate numerical references and individual browser-embedded Course checkpoints. The PR records this group's development integration; Portfolio Control closeout binds the exact merge SHA.

Final verification passed: forty independent local and forty baked HTTP comparisons; fifty-two focused geometry/physical/preservation tests including all 64 runtime corners; 290 HTTP modules; 580 desktop/mobile pages; 256 checkpoint checks; twenty cumulative DSP checks; 144 real interaction sequences/screenshots; 21 focused browser tests; 40 Robotics SVG text/legend layout checks; and 290 matching host/baked module identities. Ten plot-grid captures were visually inspected. Mandatory gates passed sequentially (contract: 103 tests in 100.19 seconds; quick: 1534 tests in 1540.79 seconds; full: 1534 tests in 1521.98 seconds). See [batch evidence](evidence/ELP-ROBOTICS-PERCEPTION-QUALITY-08-2026-09-30.md) and the [exact verification summary](course-quality/robotics-perception-verification-summary.json).

**Sixteen named findings remain, all Vehicle P01-P16: Controls 0, Robotics 0, Vehicle 16.** All three non-DSP aggregate numerical, curriculum and capstone reviews remain blocked, including courses with zero named findings. The register is non-exhaustive. This completes the requested Robotics findings, without activating Vehicle work or aggregate acceptance. DSP retains its separate authored/software aggregate review. Inventory remains 288 engineering lessons plus two examples and nine source-only repositories.

Verified read-only nonroot development preview: `http://127.0.0.1:8775`; exact image `sha256:ef29f3b77a8015d22c380cc524168cd656f77b44851aa7829f8f1177878be0fd`. Earlier final previews remain preserved. Hosted checks are recorded separately from mandatory local gates, including retained source-checkout/history failures and billing/spending limitations. Representative learners, manual screen-reader, MATLAB, hardware, concurrent capacity and production validation remain unperformed.

---

# Verified Robotics dynamics revision — 2026-09-30

ELP-ROBOTICS-DYNAMICS-QUALITY-12 repairs existing Robotics P30-P41 with executed models, independent references and twelve individually authored browser-embedded Course checkpoints. Control [PR569](https://github.com/tranquilWorks/portfolio-control/pull/569) merged before implementation at `b072a1b26e8fd608a5519737ea6b67fda0b6edb5`; the exact target baseline is PR56 merge `e8d94c521a086a93a3b595c035867c19866bbdbd`.

Verification passed: sixty independent local comparisons and sixty baked HTTP comparisons, 62 focused physical/preservation tests including all 96 runtime control corners, 290 HTTP modules, 580 desktop/mobile pages, 240 checkpoint checks, twenty cumulative DSP checks, 128 real interaction sequences/screenshots, and 21 focused browser tests. All 290 host/baked module identities match. Fourteen plot-grid captures were visually inspected; 24 selected pages passed actual SVG text-clipping and legend-overlap checks. Mandatory gates passed sequentially (contract: 103 tests in 102.48 seconds; quick: 1482 tests in 1542.87 seconds; full: 1482 tests in 1469.57 seconds). See [batch evidence](evidence/ELP-ROBOTICS-DYNAMICS-QUALITY-12-2026-09-29.md) and [exact verification summary](course-quality/robotics-dynamics-verification-summary.json). Development integration is recorded by the PR; Portfolio Control closeout binds its exact merge SHA.

**24 registered findings remain: Controls 0, Robotics 8, Vehicle 16.** The owner-authorized next group is Robotics P42-P48/P52 after this group's verified merge and a fresh exact-baseline successor contract. Vehicle P01-P16 remains outside this request. All three non-DSP aggregate numerical, curriculum and capstone reviews remain blocked, including Controls despite zero listed findings. The register is not exhaustive acceptance. Inventory remains 288 engineering lessons plus two examples and nine source-only repositories. DSP retains its separate authored/software aggregate acceptance.

Verified development preview: `http://127.0.0.1:8774`; exact read-only nonroot image `sha256:eaabddbbb6efa3fd8825075043f4623e0a6749365ac4e87efb484ed4a3f740d6`. Earlier final previews remain preserved. Temporary review containers were retired after archiving metadata/logs. Hosted CI remains separately reported: control PR569 did not start because of billing/spending limits; historical target PR56 backend failed on missing pinned source files/history (78 failed, 1328 passed, 14 errors), while its frontend passed and container job was skipped. No account, workflow or protection changes were made. Representative learners, manual screen-reader, MATLAB, hardware, concurrent capacity and production validation remain unperformed.

---

# Verified navigation and geometry revision — 2026-09-29

ELP-NAV-GEOMETRY-QUALITY-12 repairs existing Controls P56/P57/P60–P62/P64–P65 and Robotics P25–P29. All twelve now execute their declared mechanisms and include individually authored browser-embedded Course checkpoints. Contract [PR559](https://github.com/tranquilWorks/portfolio-control/pull/559) merged before implementation; the exact target baseline is PR55 merge `8820f21d349836b63db00f1e596f5eb00b488ab9`.

Verification passed: sixty independent local comparisons and sixty baked HTTP comparisons, 43 physical/preservation tests covering 96 runtime control corners, 290 HTTP modules, 580 desktop/mobile pages, 216 checkpoint checks, twenty cumulative DSP checks, 104 real interaction sequences/screenshots, and 21 focused browser tests. All 290 host/baked module identities match. Mandatory gates passed sequentially (contract: 103 tests in 100.15 seconds; quick: 1420 tests in 1424.59 seconds; full: 1420 tests in 1324.75 seconds). See [batch evidence](evidence/ELP-NAV-GEOMETRY-QUALITY-12-2026-09-29.md) and [exact verification summary](course-quality/navigation-geometry-verification-summary.json). The development PR records integration; Portfolio Control records its merge SHA after closeout.

**36 registered findings remain: Controls 0, Robotics 20, Vehicle 16.** The next repair scopes are Robotics P30–P48/P52 and Vehicle P01–P16. All three non-DSP aggregate numerical, curriculum and capstone reviews remain blocked, including Controls despite zero listed findings. This register is not exhaustive acceptance. The inventory remains 288 engineering lessons plus two examples; nine other pinned repositories remain source-only. DSP retains its separate authored/software aggregate acceptance.

Verified development preview: `http://127.0.0.1:8773`; exact read-only nonroot image `sha256:65d1de31cc56d2d3ca053ac3bdcfe0b1dae39497637dca3b4bb9b31542a1f9ee`. Earlier previews remain preserved. Hosted CI is reported separately. Representative learners, manual screen-reader, MATLAB, hardware, concurrent capacity and production validation remain unperformed. This closeout activates no further batch.

## Earlier roadmap and historical dispositions

The records below describe prior milestones. Current quality findings supersede
older whole-course acceptance language; inventory alone does not certify quality.

# Delivery Roadmap

The roadmap is a dependency-ordered set of bounded batches suitable for Portfolio Control. Each batch must produce acceptance evidence and must not claim unperformed browser, MATLAB, security, or production validation.

## B000 — Foundation vertical slice

**Outcome:** One-port platform renders discovered courses and executes a real interactive radar lesson.

- React/Vite learner shell and responsive navigation;
- declarative lesson blocks and controls;
- Plotly renderer and dataframe table;
- FastAPI catalog/runtime;
- course/module schemas and templates;
- P30 echo-ranging vertical slice;
- advanced plotting showcase;
- deterministic backend tests;
- Docker/Compose deployment.

## B010 — Contract hardening

**Depends on:** B000

- complete JSON Schemas for every nested field;
- schema migration framework and fixtures;
- semantic validation for block output references;
- course revision metadata;
- compatibility tests for version-one courses;
- generated TypeScript types from the canonical schema.

ELP-B010-01 establishes the strict current v1 boundary, semantic reference
validation, deterministic content/Git/runtime identities, generated artifact
drift checks, and Git pin/revert recovery fixtures. Historical readers and
in-place migration remain intentionally absent; any later contract increment
requires its own reviewed batch.

## ELP-DSP — Authorized item-by-item DSP/Radar conversion lane

**Depends on:** ELP-B010-01

This direct, course-owned lane converts the pinned 84-item DSP/Radar source
without modifying it and without adding DSP-specific behavior to the generic
platform:

1. `ELP-DSP-00` pins source commit
   `5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, records the immutable P01-P84
   mapping, and creates the empty native course plus conversion/evidence
   framework.
2. `ELP-DSP-P01` through `ELP-DSP-P84` create exactly one complete native
   learner module, self-contained Python runtime, and passing source-equivalence
   record in numeric order. Portfolio Control aggregate authorization
   `ELP-DSP-P01-P84` permits those 84 internal gates to be integrated as one
   target commit and one pull request; the ordered evidence and stop conditions
   remain unchanged.
3. `ELP-DSP-G-PYTHON` reviews the complete course, all equivalence and residual
   numerical records, browser/accessibility evidence, and every MATLAB
   `not_run` or `failed` result before any aggregate readiness claim.

ELP-DSP-00 establishes 84 pending, zero converted, zero blocked, and zero
placeholders. Its framework catalog is three courses,
two implemented modules, and two interactive modules because the discovered
DSP course is still empty. It does not deliver, display, or claim any converted
DSP lesson.

The ELP-DSP-P01-P84 aggregate candidate has completed the ordered software
conversion with 84 converted, zero pending, zero blocked, and zero placeholders.
Its catalog has 84 DSP/Radar modules plus the two existing platform modules.
Merge readiness remains conditional on exact-head hosted backend, frontend,
and container CI plus human review; MATLAB, browser/accessibility, learner,
physical-radar, release, deployment, and production claims remain outside the
software evidence boundary.

A blocked item stops the ordered lane. No batch may skip forward, combine
items, create bulk placeholders, mutate the pinned source, or infer MATLAB,
learner, release, deployment, production, or physical-radar evidence from a
Python conversion.

This lane is a separately authorized direct conversion sequence. It does not
implement or satisfy the generic B020 ingestion tooling or B030 author-preview
milestones below.

### ELP-DSP-FIDELITY-P02-P10 — Incremental issue-441 repair

**Status:** Implemented and locally verified as the first fidelity-remediation group.

P02-P10 replace the shared generic runtime with nine distinct source-faithful
experiments and five independently formulated scenarios per item. The repair
ledger keeps P01 as the prior distinct conversion, marks P02-P10 repaired, and
marks P11-P84 pending. Course-level numerical verification, curriculum coverage,
and capstone integration remain blocked until later issue-441 batches repair the
remaining generic modules and separately close the competency and P84 capstone gates.

### ELP-DSP-FIDELITY-P11-P20 — Fourier, spectral, and I/Q fidelity repair

**Status:** Implemented and locally verified as the second fidelity-remediation group.

P11-P20 replace ten more generic runtimes with distinct source-faithful experiments
covering FFT bins, leakage/windows, zero padding, PSD estimation, STFTs, analytic
signals, complex downconversion, signed complex sampling, I/Q correction, and noisy
tone estimation. Each item retains five independently formulated scenarios and a
named failure/recovery invariant. The ledger now records P01 already distinct,
P02-P10 repaired previously, P11-P20 repaired here, and P21-P84 pending. Issue 441
remains open and all full-course DSP/Radar maturity claims remain blocked.

## ELP-GNC — Authorized Controls/GNC conversion lane

**Depends on:** ELP-DSP-P01-P84

Portfolio Control aggregate authorization `ELP-GNC-P01-P24` advances the
read-only Controls/GNC source to
`ffd6623ee2cf8ccd8599fffd935ef07370750fa3` and converts all 24 implemented
lessons through ordered internal gates P01–P24. The retained target is one
commit and one pull request, while every item preserves its own exact source
hashes, target digest, numeric evidence, two sweeps, failure/recovery case, and
coverage transition.

The completed software course merged at
`923a86ab79893bd939d88d275bdcb12a5a1ddad6` and adds 24 native interactive
modules without changing the generic platform or the merged DSP/Radar course.
Final catalog shape is four courses, 110 modules, and 110 interactive modules.
P24 is a software-only virtual HIL plant/protocol exercise; physical HIL/HWIL
and timing claims remain outside this lane.

This direct course-owned lane does not complete B020 ingestion tooling, B030
author preview, B050 isolated execution, B070 MATLAB adapters, or B080 release
readiness.

## ELP-ORG-IDENTITY — TranquilWorks namespace normalization

**Depends on:** ELP-GNC-P01-P24

Normalize the post-transfer GitHub owner from `kpbianco` to
`tranquilWorks` for Portfolio Control, Engineering Learning Platform, all 13
submodule URLs, imported-course provenance chains, tests, current
documentation, and retained transfer evidence.

This administrative lane preserves every gitlink SHA and every course
manifest, lesson, experiment, and expected/actual numeric evidence file.
DSP/Radar remains 84/84, Controls/GNC remains 24/24, and the catalog remains
4 / 110 / 110. No unfinished course is imported or implemented by this
administrative lane. The later Robotics authorization below is separate.

## ELP-ROB-MANIPULATION-P61-P65 — Robotics manipulation and task autonomy

**Status:** Implemented and locally verified in its isolated target batch.

**Depends on:** `ELP-ROB-PLANNING-P54-P60`

This issue-440 batch implements grasp force closure, perception-guided pick/place, mobile-manipulator coordination, task-and-motion recovery, and multi-robot space-time reservations. It advances the course to 65 interactive modules and the platform catalog to 219 interactive modules. P66-P69 are delivered by the final systems/capstones batch below.

## ELP-ROB-SYSTEMS-CAPSTONES-P66-P69 — Robotics systems and capstones

**Status:** Implemented and locally verified in the final issue-440 target batch.

**Depends on:** `ELP-ROB-MANIPULATION-P61-P65`

This final batch implements typed model/frame/interface integration, deterministic timed replay with diagnosis and recovery, and two requirements-traced cumulative software capstones. Robotics closes at 69 interactive modules and the five-course catalog at 223 interactive modules. Curriculum coverage and software capstone integration pass; learner, MATLAB, browser/accessibility, and physical HIL validation remain unperformed.

## ELP-ROB — Authorized Robotics P01-P24 native Python lane

**Depends on:** ELP-ORG-IDENTITY

Portfolio Control batch `ELP-ROB-P01-P24` keeps the pinned
`robotics-autonomy-learning` source gitlink read-only at
`f8807640258f1a6c1c77f1dcc9e61734551c585b` and adds a separate
platform-owned `robotics-autonomy` course.

P01 retains and independently checks the implemented differential-drive source
design. P02-P24 retain their curriculum IDs, titles, questions, prerequisite
order, and source scaffold hashes, but their math and experiments are new
Python-first designs because the source items are non-runnable scaffolds.
NumPy supplies bounded calculations and Plotly JSON supplies the browser plots.
Independent analytic, invariant, continuous-time, or separately formulated
references check baseline and broken cases without importing production
experiments.

This batch ends at Robotics coverage 24 authored / 0 remaining / 0 blocked /
0 placeholders and catalog 5 / 134 / 134. P24 is software-only HIL methodology
and simulation, not physical HIL evidence. MATLAB runtime parity stays
`not_run`; no browser/accessibility, learner, physical robot/HIL, bench, field,
release, deployment, credential/settings, or production result is claimed.

## ELP-COURSE-CALIBER — Curriculum quality gate

**Depends on:** ELP-ROB-P01-P24

`ELP-COURSE-CALIBER-00` corrects the roadmap boundary after the initial course
conversions. The catalog totals—five courses, 134 modules, and 134 interactive
modules—remain implementation inventory only. They do not certify curriculum
coverage, capstone integration, or learner validation.

All new conversion and expansion work now requires a reviewed
competency-to-module matrix, a module count derived from that matrix, coherent
batches of no more than ten new lessons, semantic anti-template review, and
independently originated evidence. The six-stage and nine-dimension review is
defined in `docs/COURSE_CALIBER.md` and projected in
`docs/course-caliber-status.yaml`.

The audit itself created no child implementation. Controls/GNC fidelity (#438)
is completed by the separately authorized remediation below. Controls/GNC
expansion (#439), Robotics expansion (#440), and DSP/Radar fidelity (#441)
remain separately owned work. Vehicle Dynamics preparation is now separately
authorized under issue #467; lesson work still requires its own coherent
at-most-ten-lesson batch.

## ELP-GNC-FIDELITY — Controls/GNC P01-P24 remediation

**Depends on:** ELP-COURSE-CALIBER-00

Issue #438 repairs the existing 24-item Controls/GNC implementation without
adding curriculum. Every item retains exact source identity, a semantic map,
two one-variable sweeps, a named broken/recovery path, limiting cases, explicit
omissions, domain-specific axes, and five independently originated numerical
comparisons. P01 uses the pinned source's explicit-Euler failure step; P24 uses
two timestamped transport directions and source-ordered same-tick delivery.

Controls/GNC advances to `numerically_verified: passed` at a deterministic
software-only boundary. Curriculum coverage and capstone integration remain
partial, learner validation remains unperformed, and issue #439 is the sole
owner of later Controls/GNC expansion. The batch does not execute MATLAB,
validate browser accessibility or learners, operate physical HIL, or authorize
release, deployment, credentials/settings, or production use.

## ELP-GNC-EXPANSION — Competency-derived Controls/GNC P25-P68

**Depends on:** ELP-GNC-FIDELITY-P01-P24

Issue #439 derives a 68-module course from a reviewed competency and prerequisite map rather than a fixed lesson quota. The 44 native Python additions are divided into coherent batches of 9, 9, 9, 5, 6, 3, and 3 lessons. P25-P68 now implement the complete mapped sequence, including three requirements-traced cumulative capstones, with independent five-scenario evidence.

The final three lessons are cumulative capstones: identification/control/estimation under uncertainty; navigation/guidance of a constrained survey; and a requirements-traced faulted software-HIL GNC loop. Every issue-439 batch and capstone is implemented and locally verified. Native additions do not claim MATLAB/source equivalence, and the entire lane remains software-only.

## ELP-VEHICLE-PREP-00 — Vehicle Dynamics governed preparation

**Status:** Complete; P01-P67 implemented in eight separately authorized batches.

**Depends on:** `ELP-ROB-SYSTEMS-CAPSTONES-P66-P69`

Issue #467 derives 67 modules from the reviewed competency graph and partitions
them into eight coherent batches of at most ten lessons. This prep batch advances
only the read-only source gitlink, installs the exact 24-item source and coverage
ledgers, mirrors the reviewed map, and adds deterministic synthetic GR86
CAN/RaceChrono BLE protocol fixtures with independent decode and fault checks.

The completed implementation catalog has six courses, 290 modules, and 290 interactive modules;
Vehicle Dynamics contributes P01-P67. The fixture and all identification inputs are synthetic, not measured vehicle
data, and do not validate firmware, radio, bench, vehicle, track, or physical
HIL behavior. `ELP-VEHICLE-P01-P08`, `ELP-VEHICLE-P09-P16`, and
`ELP-VEHICLE-P17-P24`, `ELP-VEHICLE-TIRES-P25-P33`, and
`ELP-VEHICLE-CHASSIS-P34-P43`, `ELP-VEHICLE-PROPULSION-P44-P52`, and `ELP-VEHICLE-TELEMETRY-P53-P60` each have exact Portfolio Control authorization against
their merged predecessor. P01-P60 now
provide distinct bounded models, independent scalar references, five-scenario
evidence, named failures, and exact recoveries. P20 is explicitly a synthetic
offline stand-in despite its retained title, and P24 is a software-only GR86
baseline. P25-P33 deepen tire competencies; P34-P43 deepen handling, stability,
load-transfer, ride, damping, suspension, and anti-geometry competencies. P44-P52
deepen traction, launch, differential, gearing, braking, aero-balance, and stint-limit
competencies without altering the source-bound ledger. P53-P60 deepen telemetry replay, timing, calibration, reconstruction, estimation, identification, uncertainty, and fault recovery. P61-P67 close performance analysis and two cumulative capstones.

## B020 — Course ingestion and migration tooling

**Depends on:** B010

- `elp inspect-course PATH` readiness report;
- MATLAB-first module inventory scanner;
- scaffold generator for `course.yaml`, `module.yaml`, and migration notes;
- golden-vector file convention;
- no-write dry-run by default;
- explicit author-owned apply mode.

## B030 — Author preview and component gallery

**Depends on:** B010

- live reload across mounted course directories;
- schema-aware author diagnostics in the browser;
- searchable component/plot gallery;
- responsive visual regression fixtures;
- accessibility regression suite;
- module state permalink/export.

## B040 — Large numerical data transport

**Depends on:** B010

- Apache Arrow IPC artifact endpoint;
- Parquet dataset references;
- bounded artifact lifetime and cleanup;
- server-side downsampling/tiling contracts;
- virtualized tables;
- large heatmap/range–Doppler performance tests.

## B050 — Isolated execution workers

**Depends on:** B010

- queue-backed subprocess/container worker;
- hard CPU/memory/wall-clock limits;
- no-network execution profile;
- result and artifact quotas;
- cancellation and stale-run suppression;
- concurrency/fairness tests;
- worker health and telemetry.

## B060 — Progress, assessments, and SSO

**Depends on:** B030, B050

- reverse-proxy identity contract;
- learner progress separate from canonical course content;
- prediction/check responses;
- completion and teach-back evidence;
- role model for learner, author, reviewer, administrator;
- export/delete/retention policy.

## B070 — Runtime adapters

**Depends on:** B050

- remote Python/GPU worker;
- optional MATLAB Engine worker with license/capacity controls;
- optional browser WASM kernels;
- adapter conformance tests against one result envelope;
- golden-vector parity reporting.

## B080 — Corporate release readiness

**Depends on:** B040, B050, B060

- deployment manifests for the chosen corporate platform;
- SBOM, signing, scans, and offline dependency mirroring;
- structured logging and OpenTelemetry;
- backup/restore for learner progress;
- load test and capacity envelope;
- rollback rehearsal;
- operations runbook.

## B090 — First course migrations

**Depends on:** B020, B030

For courses outside the dedicated DSP/Radar and Controls/GNC lanes, migrate representative
modules before attempting every course:

1. one 3-D/heatmap-heavy engineering module;
2. one static/media-heavy module;
3. one course that stresses large data transport.

Use those pilots to revise the schema and authoring workflow before bulk conversion.
The separate ELP-DSP sequence above does not mark B020, B030, or this broader
cross-course migration milestone complete.

### ELP-DSP-FIDELITY-P21-P28 — Modulation, channels and statistical evidence

Continue from merged replay repair PR #45 under control PR #503. The eight
source-specific experiments replace generic runtime behavior for AM/FM,
constellations, RRC/matched filtering, multipath equalization, LMS cancellation,
Monte Carlo confidence and ROC/estimation. Each retains five independent scenarios,
physical controls, explicit failure/recovery and finite-resource limits.

Preserve P01-P20 and P29-P84 byte-identically. After verification, issue 441
continues at P29; full-course numerical, curriculum and capstone claims remain
blocked. MATLAB, browser/learner, hardware and deployment are separate gates.

## DSP/Radar twelve-item fidelity continuation P29-P40 — 2026-09-27

Owner approved merge of PR #46 and requested twelve lessons per batch. Active
contract `ELP-DSP-FIDELITY-P29-P40`, authorized by control PR #505, repairs the
radar foundations through integration as one reviewable unit. Preserve P01-P28
and P41-P84, retain sixty independent numerical scenarios and all local gates.
P41-P52 is the next proposed twelve-item group after completion/merge and its
own scoped contract. These repair existing lessons; no inventory expansion or
whole-course maturity claim follows from batch size.

## DSP/Radar twelve-item fidelity continuation P41-P52 — 2026-09-27

Merged target PR #47 establishes baseline `f78831b23e46ff1cb9518a716ac8ba5aeab5a3ee`.
Control PR #508 authorizes `ELP-DSP-FIDELITY-P41-P52`: clutter/Swerling, full
range-Doppler processing, fixed thresholds, ROC and CFAR calibration/window/
stress/Monte Carlo experiments. Preserve P01-P40 and P53-P84 and retain sixty
independent scenarios. P53-P64 is the next proposed twelve-lesson group after
this batch is verified, merged and separately contracted. Issue 441 stays open.


## DSP/Radar twelve-item fidelity continuation P53-P64 — 2026-09-27

Merged target PR #48 establishes baseline `255427e3b3c6a31a66b74ad7f9836dad09b164e5`.
Control PR #515 authorizes `ELP-DSP-FIDELITY-P53-P64`: report grouping,
alpha-beta/Kalman/EKF tracking, association/lifecycle/crossing/IMM, and ULA
steering, array factor, DAS and amplitude-comparison monopulse. Preserve
P01-P52 and P65-P84 and retain sixty independent scenarios. P65-P76 is the next
proposed twelve-lesson group after this batch completes and merges under its
own fresh contract. Whole-course maturity remains blocked; issue 441 stays open.

- `ELP-DSP-FIDELITY-P65-P76`: owner-requested twelve-lesson continuation after
  PR #49. Repair adaptive arrays, FMCW, MIMO, micro-Doppler and initial SAR
  processing with independent five-scenario evidence. P77-P84 remain pending;
  course-level numerical/curriculum/capstone maturity and issue441 remain open.


## DSP/Radar final fidelity group P77-P84 — 2026-09-28

Merged PR #50 establishes baseline `f05403ef2c0a5e31d7045c0cb796b2e136ca50c9`.
Control PR #523 authorizes `ELP-DSP-FIDELITY-P77-P84`: SAR backprojection,
migration, resolution and autofocus, ISAR, passive cross-ambiguity, STAP and
the end-to-end radar capstone. Forty independent scenarios complete the item
repair inventory: one distinct, seventy-five prior repairs, eight current, zero
pending. Preserve P01-P76 and source/platform identities. No further lesson
batch follows automatically; aggregate caliber, competency mapping and cumulative
assessment are the next separate review under issue 441. Whole-course numerical,
curriculum and capstone maturity remains blocked pending that review.

## ELP-GNC-SEMANTIC-QUALITY-12 — twelve existing Controls model repairs

Exact predecessor: PR54 merge `00983cab0599b1ce3a613a2cc8ef42eb7b45f0b4`.
Control contract: PR551, `6d81736bba58cc05f6ccc78e4a3ad66386d731bb`.
Scope: P36/P38/P42/P43/P45–P51/P55, preserving all other course payloads and the
prerequisite graph. Actual mechanisms, independently generated numerical cases,
physical tests and twelve Course checkpoints are implemented. Selected browser
verification, the final 580-page whole-container sweep and all mandatory local
gates passed. The batch evidence retains exact results and development PR tracking.
Forty-eight findings remain blocked after these scoped closures. This batch adds
no lessons and does not promote Controls/Robotics/Vehicle aggregate acceptance.

## Navigation and geometry revision (2026-09-29)

Twelve existing lessons now have executed mechanisms, independent references and embedded checkpoints. Full baked delivery and sequential contract/quick/full gates passed; the development PR and Portfolio Control closeout record integration. Remaining registered work is Robotics P30–P48/P52 and Vehicle P01–P16, plus separate non-DSP aggregate reassessments. Zero listed Controls findings does not authorize blanket acceptance or a new content expansion.


---

## ELP-BREADTH-GENERALIST-00 — Generalist engineering, physics and mathematics survey curriculum

**Status:** Roadmap-only scope. Not an active implementation batch. No course inventory, source pin, schema, runtime, active-batch contract, or maturity claim is changed by this section.

**Intent:** Add a broad awareness layer around the existing depth curricula so a learner can become a technically literate, cross-disciplinary systems engineer: able to look at an unfamiliar physical or engineered system, identify the governing domains, reason from first principles, estimate orders of magnitude, interpret the important plots and measurements, recognize failure modes and unsafe assumptions, and know when a specialist or an existing depth track is required.

The target is deliberately different from a conventional degree sequence. Each breadth course compresses roughly the conceptual coverage of an introductory 100/200-level university sequence into a small number of substantial interactive lessons. The learner should not be expected to reproduce long derivations, prove theorems, or execute specialist design calculations from memory. Equations remain visible and dimensioned, but the emphasis is on physical meaning, relationships, scaling, model boundaries, interpretation and systems consequences.

The motivating end state is a resilient technical generalist: the person who can reason about structures, mechanisms, fluids, heat, power, electronics, materials, water, machinery, sensing, infrastructure, biology and computation well enough to diagnose a problem, communicate across disciplines and choose a credible next step under normal or resource-constrained conditions. This is the "ultimate systems engineer / field engineer" objective, not a claim of professional mastery in every discipline.

### Relationship to the existing depth curricula

The following existing repositories remain the depth layer and MUST NOT be replaced by parallel breadth courses:

- Controls/GNC — controls-gnc-learning
- Distributed real-time systems — distributed-realtime-learning
- Embedded real-time/HIL — embedded-rt-hil-learning
- Flight dynamics — flight-dynamics-learning
- FPGA data paths — fpga-data-path-learning
- HWIL/test systems — hwil-systems-learning
- Numerical optimization — numerical-optimization-learning
- Reliability/FDIR — reliability-fdir-learning
- RF laboratory / applied RF — rf-lab-learning
- Robotics/autonomy — robotics-autonomy-learning
- Statistics/estimation — stats-estimation-learning
- Vehicle dynamics — vehicle-dynamics-learning
- DSP/radar — dsp-radar-learning

The native DSP/Radar, Controls/GNC, Robotics/Autonomy and Vehicle Dynamics courses likewise remain depth-owned. The nine source-only repositories are also reserved for their eventual depth conversions. Breadth material may introduce vocabulary or a prerequisite concept that touches these areas, but it should terminate in an explicit handoff rather than recreate the depth curriculum.

Examples:

- A circuits lesson may explain sampling and aliasing at an awareness level, then hand off to DSP/Radar for real signal-processing depth.
- An aerodynamics lesson may explain stability derivatives conceptually, then hand off to Flight Dynamics for aircraft equations of motion and control.
- A sensors lesson may explain accelerometers and gyros, then hand off to Stats/Estimation and Controls/GNC for filtering and navigation.
- A safety lesson may introduce FMEA and fault trees, then hand off to Reliability/FDIR for rigorous reliability engineering.
- A digital systems lesson may explain FPGA architecture, then hand off to FPGA Data Path for implementation depth.
- A systems lesson may explain HIL/HWIL roles, then hand off to the Embedded RT/HIL and HWIL Systems tracks for execution depth.

### Breadth-course time box and learner pace

The breadth layer is intentionally designed for a **single-weekend learning session**, not a semester-equivalent workload disguised as a short course.

Planning targets:

- **2–6 learner hours per breadth course**, with approximately **4 hours as the default design point**;
- normally **12–20 concise modules**, with the module count driven by the competency map rather than padding;
- approximately **8–15 minutes of active learner time per ordinary module**;
- approximately **20–30 minutes for a final systems-engineer challenge**;
- no required multi-week homework, long derivation sets, literature reviews, memorization-heavy exams or specialist implementation projects;
- a learner should normally be able to start and finish one breadth course over one weekend, even if they split it across two sittings.

Across the currently scoped 56 breadth courses, this implies roughly **112–336 learner hours total**, with a central planning estimate near **224 hours**. At a pace of about one course per weekend, the complete breadth layer is intentionally a roughly **one-year to fourteen-month journey**, not another four-year degree program.

The time box is a curriculum constraint, not merely an estimate. If a proposed breadth course cannot credibly teach its recognition/reasoning outcomes inside the 2–6 hour envelope, authors should first:

1. remove specialist derivations or repetitive calculation practice;
2. replace procedural math with visual, dimensional or computational intuition;
3. merge duplicated concepts;
4. move implementation-level material to an existing depth course or an explicit future depth handoff;
5. split the domain only when it contains genuinely distinct systems-level competencies that cannot be understood coherently as one survey.

Rare exceptions above six hours require explicit competency-map justification. "The university version takes a semester" is not sufficient justification: the breadth course is intentionally teaching a different level of mastery.

The learner outcome after a weekend is **domain literacy and first-principles orientation**, not professional qualification. The learner should be able to say, for example, "I understand what metacentric stability means, how moving the center of gravity affects a ship, what a righting-arm curve tells me, and what evidence I would need next" without being expected to perform a naval architect's complete stability analysis.

### End-of-course systems-engineer challenge

Every breadth course should end with one short, unfamiliar scenario that forces the learner to synthesize the course rather than repeat isolated lesson facts. Target duration is **20–30 minutes**.

The challenge should ask the learner to do several of the following:

- identify the governing domains and physical laws;
- sketch the important energy, force, material, information or heat flows;
- identify the quantities and units that matter;
- make one or more order-of-magnitude estimates;
- interpret a provided plot, schematic, measurement set or operating envelope;
- identify plausible failure modes and eliminate at least one tempting but incorrect explanation;
- choose the next useful measurement or experiment;
- identify an unsafe assumption or stop-work condition;
- state which neighboring discipline or depth track should take over next.

These are reasoning exercises, not miniature professional certification problems. A Marine Engineering challenge might present a vessel with a changed cargo configuration, persistent roll and speed-dependent propeller vibration; the learner would reason across stability, encounter frequency, propulsion/cavitation and measurement choices without being asked to produce a class-approved stability booklet.

### Breadth-course learning contract

Every breadth course should satisfy the following learning outcomes.

A learner who completes a course should be able to:

1. name the principal quantities, units, state variables and conserved quantities;
2. identify the governing laws and explain what they mean physically;
3. recognize the dominant effects and the conditions under which a simpler model is acceptable;
4. read the domain's common plots, diagrams, schematics and tables;
5. perform rough dimensional, scaling and order-of-magnitude checks;
6. predict the direction of change when one important parameter is varied;
7. identify common failure modes, singularities, unstable regions and unsafe assumptions;
8. choose the next useful measurement, experiment or source of evidence;
9. explain the interfaces to neighboring disciplines;
10. state clearly what the survey does NOT qualify the learner to design, certify or operate.

### Lesson format

Planning target: normally 12–20 substantial lessons per breadth course and 2–6 total learner hours including the final challenge. This is a target range, not a quota; final counts MUST come from a reviewed competency-to-module map under the existing Course Caliber rules. A module should usually be short enough to complete in roughly 8–15 active minutes; several pages of readable material are acceptable when they remain concise and skimmable.

A typical lesson should contain:

- several pages of concise narrative rather than a one-screen summary;
- one governing relation or model family, with every symbol and unit explained;
- an optional collapsed derivation for learners who want the math;
- one worked estimation or back-of-the-envelope example;
- one prediction before interaction;
- one useful interactive model, diagram, plot, geometry manipulation or failure-mode toggle when the subject permits it;
- at least one limiting case or "when this model breaks" example;
- one interpretation task based on actual plotted or tabulated evidence;
- one short check that tests reasoning rather than formula memorization;
- an explicit cross-course handoff where deeper treatment already exists.

The breadth layer should prefer dimensional reasoning, graphs, geometry, ratios, conservation laws and qualitative differential-equation behavior over algebraic grind. Calculus, differential equations, tensors, complex numbers and statistics may appear whenever they clarify the physics, but a learner should be able to complete the survey without becoming fluent at symbolic manipulation.

A breadth lesson should not expand merely because the source discipline normally assigns substantial homework. Worked mathematics exists to reveal behavior, scales and tradeoffs. Repetitive symbolic practice, long proofs, software implementation drills and professional design workflows belong in depth curricula or optional enrichment. The governing question is whether the learner can **recognize, reason, estimate, diagnose and communicate**, not whether they can reproduce a textbook problem set.

### Suggested interaction vocabulary

The platform should reuse a small set of high-value interaction patterns across breadth courses without making the subject matter generic:

- parameter sweep with immediate dimensional plots;
- "predict then reveal";
- limit-case slider;
- failure/recovery toggle;
- geometry or free-body manipulation;
- energy/material/flow budget;
- field-line, mode-shape, streamline or vector-field visualization;
- phase diagram or operating-envelope navigation;
- before/after comparison;
- unit and scale sanity check;
- choose-the-next-measurement diagnostic;
- subsystem interface map;
- scenario triage under a constrained resource budget.

### Mathematics breadth

#### B-MATH-01 — Mathematical language, scaling and modeling

Purpose: make the learner comfortable translating physical statements into quantities and relationships before deeper mathematics appears.

Candidate lessons:

1. quantities, units, dimensions and dimensional consistency;
2. algebraic relationships, functions and inverse functions;
3. powers, exponentials, logarithms and orders of magnitude;
4. ratios, proportionality, similarity and scaling laws;
5. trigonometry and the geometry of components;
6. analytic geometry and coordinate systems;
7. vectors, dot products and cross products at a physical-intuition level;
8. complex numbers as magnitude/phase objects;
9. sequences, series and convergence intuition;
10. inequalities, bounds and envelope reasoning;
11. nondimensionalization and dimensionless groups;
12. approximation, linearization and small-parameter reasoning;
13. sensitivity, conditioning and "which variable matters?";
14. Fermi estimates and engineering sanity checks;
15. model assumptions, abstraction levels and choosing the simplest useful model.

Representative interactions: unit-consistency checker, scaling-law sandbox, log/linear plot comparison, sensitivity sliders, Fermi-estimation exercises.

#### B-MATH-02 — Calculus, vector calculus and differential equations

Purpose: understand the language used to describe continuous change without requiring a traditional calculation-heavy calculus sequence.

Candidate lessons:

1. limits and local behavior;
2. derivatives as rates, slopes and sensitivity;
3. integrals as accumulation, area and conserved totals;
4. the fundamental theorem of calculus conceptually;
5. multivariable functions and partial derivatives;
6. gradients and directional change;
7. Jacobians and Hessians as local maps/curvature descriptors;
8. line integrals and work;
9. surface/volume integrals and flux;
10. divergence and curl;
11. first-order ODEs and time constants;
12. second-order ODEs, natural frequency and damping;
13. coupled ODE systems and state variables;
14. initial conditions, boundary conditions and well-posedness;
15. PDE families: elliptic, parabolic and hyperbolic behavior;
16. Laplace, diffusion/heat and wave equations as archetypes;
17. transforms as tools for changing representation, with DSP/controls handoffs;
18. qualitative versus numerical solution methods.

Representative interactions: tangent/accumulation visualizer, gradient field, divergence/curl field, ODE response explorer, PDE propagation/diffusion comparison.

#### B-MATH-03 — Linear algebra, tensors and engineering geometry

Candidate lessons:

1. vectors, matrices and linear transformations;
2. systems of linear equations and rank;
3. bases, coordinates and change of basis;
4. orthogonality, projections and inner products;
5. least-squares geometry, with Stats/Estimation handoff;
6. eigenvalues and eigenvectors;
7. modes and diagonalization intuition;
8. singular-value decomposition;
9. conditioning, singularity and observability intuition;
10. quadratic forms and energy ellipsoids;
11. coordinate frames and homogeneous transformations;
12. rotations in 2-D and 3-D;
13. tensors as multi-directional physical properties;
14. principal axes and tensor invariants;
15. differential geometry and manifolds as a map of curved state/configuration spaces;
16. geometry handoffs to Controls/GNC, Robotics and solid/continuum mechanics.

Representative interactions: matrix-as-transformation visualizer, eigenmode explorer, SVD image/geometry decomposition, principal-axis rotation.

#### B-MATH-04 — Discrete mathematics, logic, graphs and coding concepts

Candidate lessons:

1. sets, relations and functions;
2. propositional and predicate logic;
3. Boolean algebra and logic circuits;
4. proof styles and what a proof establishes;
5. counting, permutations and combinations;
6. recurrence relations and discrete-time evolution;
7. graph vocabulary and graph traversal;
8. trees, spanning trees and hierarchical structures;
9. network flows and connectivity;
10. finite-state machines;
11. discrete geometry and computational geometry;
12. number-theory concepts used in computation/cryptography;
13. error detection and coding-theory intuition;
14. computational complexity and tractability;
15. discrete-model handoffs to computer systems, networking, FPGA and algorithms.

#### B-MATH-05 — Higher mathematics map: analysis, algebra, geometry and topology

Purpose: provide recognition-level literacy in the major branches of higher mathematics so later technical literature is not opaque.

Candidate lessons:

1. real analysis: rigor, continuity and convergence;
2. measure theory and generalized integration;
3. complex analysis and analytic functions;
4. contour integration and residues as an engineering tool;
5. functional analysis and infinite-dimensional spaces;
6. Hilbert/Banach-space intuition;
7. operator theory and eigen-operators;
8. distributions/generalized functions and impulses;
9. harmonic analysis and transforms, with DSP handoff;
10. calculus of variations;
11. abstract algebra: groups, rings and fields;
12. modules, commutative algebra and homological algebra as a conceptual map;
13. Galois theory and symmetry of equations;
14. Lie groups and Lie algebras;
15. representation theory and symmetry;
16. differential geometry;
17. topology, algebraic topology and invariants;
18. algebraic/projective geometry and where these abstractions appear in modern engineering/physics.

#### B-MATH-06 — Nonlinear dynamics, asymptotics and applied mathematical systems

Candidate lessons:

1. dynamical systems and phase space;
2. equilibria and local stability;
3. phase portraits and nullclines;
4. limit cycles and self-sustained oscillation;
5. bifurcations and qualitative regime change;
6. chaos, sensitivity and attractors;
7. perturbation methods;
8. asymptotic expansions and dominant balance;
9. singular perturbations and multiple time scales;
10. variational reasoning;
11. decision theory;
12. game theory;
13. queueing theory;
14. information theory concepts and entropy, with DSP handoff;
15. network science and complex systems;
16. stochastic-process concepts, with Stats/Estimation handoff;
17. nonlinear-system handoff to Controls/GNC.

#### B-MATH-07 — Numerical and computational methods

Candidate lessons:

1. floating-point representation and numerical error;
2. truncation, roundoff and conditioning;
3. root finding;
4. interpolation and approximation;
5. numerical differentiation;
6. numerical integration;
7. explicit and implicit ODE integration;
8. stiffness and solver selection;
9. numerical linear algebra;
10. numerical eigenvalue problems;
11. nonlinear systems of equations;
12. finite-difference methods;
13. finite-volume methods;
14. finite-element methods;
15. spectral methods;
16. Monte Carlo simulation;
17. mesh/refinement and convergence studies;
18. verification versus validation;
19. scientific computing and high-performance-computing awareness;
20. optimization handoff to Numerical Optimization.

### Physics breadth

#### B-PHYS-01 — Classical mechanics and analytical mechanics

Candidate lessons:

1. position, velocity and acceleration;
2. Newton's laws and force models;
3. free-body reasoning;
4. work and kinetic energy;
5. potential energy and conservative systems;
6. linear momentum and impulse;
7. angular momentum;
8. rotational inertia and rigid-body rotation;
9. rolling, friction and contact;
10. collisions and impact;
11. constraints and generalized coordinates;
12. non-inertial frames and fictitious forces;
13. gyroscopes and precession;
14. Lagrangian mechanics;
15. Hamiltonian mechanics;
16. orbital and celestial-mechanics intuition;
17. many-body and continuum bridges;
18. limits of classical mechanics.

#### B-PHYS-02 — Oscillations, waves, vibration physics and acoustics

Candidate lessons:

1. simple harmonic motion;
2. damping and forced response;
3. resonance, bandwidth and Q;
4. coupled oscillators and normal modes;
5. the wave equation and propagation speed;
6. reflection, transmission and impedance;
7. superposition and interference;
8. standing waves and resonators;
9. phase velocity, group velocity and dispersion;
10. nonlinear-wave awareness;
11. sound pressure, intensity and decibels;
12. room/architectural acoustics;
13. underwater acoustics;
14. ultrasonics;
15. aeroacoustics and noise generation;
16. shock waves;
17. seismology as wave physics;
18. vibration/acoustic measurement and interpretation.

#### B-PHYS-03 — Electricity and magnetism

Candidate lessons:

1. charge and Coulomb forces;
2. electric fields and flux;
3. potential and voltage;
4. capacitance and dielectric behavior;
5. current, resistance and conduction;
6. magnetic fields and magnetic forces;
7. magnetic materials;
8. electromagnetic induction;
9. inductance and stored magnetic energy;
10. Maxwell's equations as the unifying picture;
11. electromagnetic waves;
12. Poynting flow and field energy;
13. boundary conditions and material interfaces;
14. conductors, dielectrics and skin-depth intuition;
15. transmission-line and waveguide concepts;
16. radiation and scattering concepts;
17. EMC/EMI awareness;
18. handoff to RF Lab, DSP/Radar and optics.

#### B-PHYS-04 — Optics and photonics

Candidate lessons:

1. ray optics and Fermat's principle;
2. lenses, mirrors and imaging;
3. aberrations and resolution;
4. wave optics;
5. interference;
6. diffraction;
7. polarization;
8. coherence and statistical optics;
9. Fourier optics and spatial frequency;
10. lasers and resonators;
11. nonlinear optics;
12. fiber optics;
13. integrated photonics;
14. optical communications concepts;
15. spectroscopy;
16. interferometry and precision measurement;
17. radiometry and photometry;
18. holography;
19. electro-optics and acousto-optics;
20. lidar/imaging-system awareness.

#### B-PHYS-05 — Quantum mechanics, atomic and molecular physics

Candidate lessons:

1. why classical physics fails at small scales;
2. wavefunctions and probability amplitudes;
3. the Schrödinger equation conceptually;
4. particles in wells and quantized states;
5. tunneling;
6. the quantum harmonic oscillator;
7. uncertainty and noncommuting observables;
8. spin and angular momentum;
9. measurement and state preparation;
10. entanglement and correlations;
11. identical particles and statistics;
12. atomic structure and orbitals;
13. molecular bonding and molecular states;
14. rotational/vibrational spectra;
15. laser-atom interaction;
16. cold atoms and Bose-Einstein condensates;
17. atomic clocks and precision measurement;
18. quantum information/computing;
19. quantum sensing and communication;
20. handoff to quantum optics and solid-state physics.

#### B-PHYS-06 — Condensed matter and solid-state physics

Candidate lessons:

1. bonding and crystal structures;
2. lattices, reciprocal-space intuition and diffraction;
3. crystal defects;
4. lattice vibrations and phonons;
5. electron bands;
6. conductors, insulators and semiconductors;
7. carrier transport;
8. junction and device-physics bridge;
9. dielectric response;
10. magnetism;
11. superconductivity;
12. ferroelectric and piezoelectric materials;
13. spintronics;
14. surfaces and interfaces;
15. thin films;
16. nanophysics and mesoscopic systems;
17. soft matter and polymer physics;
18. quantum materials.

#### B-PHYS-07 — Nuclear, particle and radiation physics

Candidate lessons:

1. nuclear structure and binding energy;
2. radioactive decay;
3. alpha, beta, gamma and neutron interactions;
4. radiation attenuation in matter;
5. detectors and counting statistics conceptually;
6. radiation dose and biological-effect units;
7. nuclear reactions;
8. neutron physics;
9. fission physics;
10. fusion physics;
11. accelerator principles;
12. elementary particles and interactions;
13. the Standard Model;
14. neutrinos;
15. collider/high-energy physics;
16. cosmic rays;
17. radiation shielding principles;
18. handoff to Nuclear Engineering.

#### B-PHYS-08 — Relativity, gravitation and cosmology

Candidate lessons:

1. reference frames and the speed of light;
2. special relativity postulates;
3. spacetime diagrams;
4. time dilation and length contraction;
5. relativistic momentum and energy;
6. relativistic electrodynamics awareness;
7. the equivalence principle;
8. curved spacetime;
9. gravitational time dilation;
10. relativistic orbits and lensing;
11. black holes;
12. gravitational waves;
13. the expanding universe;
14. cosmological history;
15. dark matter and dark energy;
16. practical timing/GNSS consequences.

#### B-PHYS-09 — Plasma physics and magnetohydrodynamics

Candidate lessons:

1. ionization and plasma criteria;
2. Debye shielding;
3. plasma frequency and collective behavior;
4. single-particle motion in fields;
5. collisions and transport;
6. plasma fluid models;
7. plasma waves;
8. instabilities;
9. sheaths and boundaries;
10. magnetohydrodynamics;
11. magnetic confinement;
12. inertial/fusion-plasma concepts;
13. space plasmas;
14. industrial plasmas;
15. plasma propulsion;
16. diagnostic concepts.

#### B-PHYS-10 — Earth, atmosphere, ocean and space environment

Candidate lessons:

1. Earth's internal structure and geodynamics;
2. plate tectonics;
3. seismic waves and earthquake physics;
4. gravity, geodesy and Earth's figure;
5. geomagnetism;
6. atmospheric structure and thermodynamics;
7. weather systems and fronts;
8. clouds, precipitation and convection;
9. climate energy balance and feedback;
10. ocean structure and circulation;
11. surface waves and tides;
12. hydrologic cycle;
13. cryosphere;
14. remote sensing across optical/thermal/radar modalities;
15. solar physics;
16. heliosphere and solar wind;
17. magnetosphere and space weather;
18. planetary science and comparative environments.

### Mechanical, thermal and aerospace breadth

#### B-MECH-01 — Statics, mechanics of materials and structural mechanics

Candidate lessons:

1. forces, moments and equilibrium;
2. free-body diagrams for structures;
3. trusses and frames;
4. shear-force and bending-moment diagrams;
5. stress and strain;
6. axial loading;
7. torsion;
8. beam bending;
9. combined loading;
10. stress transformation and principal stresses;
11. deflection and stiffness;
12. energy methods;
13. buckling and stability;
14. elasticity, plasticity and viscoelasticity;
15. fracture mechanics;
16. fatigue and creep;
17. contact mechanics;
18. structural dynamics and FEA handoffs.

Representative interactions: movable-load beam diagram, truss-force visualization, stress/strain material comparison, buckling mode explorer.

#### B-MECH-02 — Dynamics, mechanisms and rotating machinery

Candidate lessons:

1. particle kinematics;
2. particle kinetics;
3. rigid-body planar kinematics;
4. rigid-body kinetics;
5. work-energy methods;
6. impulse-momentum methods;
7. linkages and mechanisms;
8. cams and followers;
9. gears and gear trains;
10. flywheels and energy smoothing;
11. balancing rotating masses;
12. vibration isolation;
13. multi-degree-of-freedom modes;
14. rotordynamics and critical speed;
15. gyroscopic effects;
16. multibody-system awareness;
17. impact mechanics;
18. handoffs to Vehicle Dynamics and Robotics.

#### B-MECH-03 — Thermodynamics

Candidate lessons:

1. systems, control volumes and state;
2. temperature, pressure and properties;
3. work and heat;
4. first-law energy balances;
5. enthalpy and flow work;
6. ideal and real gases;
7. mixtures and humidity concepts;
8. second law and entropy;
9. reversibility, irreversibility and exergy;
10. phase diagrams and phase change;
11. Carnot and ideal cycle limits;
12. Rankine steam cycles;
13. Brayton gas-turbine cycles;
14. Otto/Diesel engine cycles;
15. refrigeration and heat-pump cycles;
16. combustion thermodynamics;
17. chemical thermodynamics;
18. statistical and nonequilibrium thermodynamics awareness.

#### B-MECH-04 — Heat transfer and mass transfer

Candidate lessons:

1. conduction and Fourier's law;
2. thermal resistance networks;
3. fins and extended surfaces;
4. transient conduction;
5. convection and boundary layers;
6. internal forced convection;
7. external forced convection;
8. natural convection;
9. dimensionless heat-transfer groups;
10. thermal radiation;
11. view factors and enclosure radiation;
12. heat exchangers;
13. boiling;
14. condensation;
15. diffusion and Fick's law;
16. convection-diffusion;
17. coupled heat/mass transport;
18. thermal-management trade studies.

#### B-MECH-05 — Fluid mechanics, hydraulics and flow systems

Candidate lessons:

1. fluid properties and constitutive behavior;
2. pressure and hydrostatics;
3. buoyancy and stability;
4. continuity and mass conservation;
5. control-volume momentum;
6. Bernoulli/energy equations;
7. viscosity and shear;
8. laminar versus turbulent flow;
9. pipe flow and head loss;
10. fittings, valves and network losses;
11. pumps and fans;
12. dimensional analysis and similitude;
13. boundary layers;
14. drag/lift as fluid-force outcomes;
15. open-channel flow;
16. compressible-flow introduction;
17. multiphase and non-Newtonian flow;
18. cavitation and vapor formation;
19. rarefied-gas awareness;
20. CFD handoff.

#### B-MECH-06 — Mechanical design and machine elements

Candidate lessons:

1. design requirements, loads and factors of safety;
2. fasteners and bolted joints;
3. rivets, pins and mechanical joints;
4. shafts and keys/splines;
5. rolling and sliding bearings;
6. gears;
7. belts, chains and flexible drives;
8. springs;
9. seals and gaskets;
10. pressure-containing components;
11. welded-joint design concepts;
12. lubrication and tribology;
13. fits, clearances and tolerances;
14. fatigue-aware machine design;
15. hydraulic actuators;
16. pneumatic actuators;
17. motor/actuator selection interfaces;
18. maintainability, repairability and graceful failure.

#### B-MECH-07 — Manufacturing, fabrication, tolerancing and metrology

Candidate lessons:

1. manufacturing process selection;
2. turning;
3. milling and drilling;
4. grinding and finishing;
5. EDM;
6. laser and waterjet processing;
7. casting;
8. forging;
9. sheet-metal forming;
10. extrusion and drawing;
11. welding;
12. brazing and soldering;
13. additive manufacturing;
14. injection molding;
15. composite manufacturing;
16. heat treatment and surface treatment;
17. dimensional tolerancing and GD&T;
18. metrology and inspection;
19. CNC/CAM/tooling concepts;
20. DFM/DFA, process capability and quality.

#### B-MECH-08 — HVAC, refrigeration and building mechanical systems

Candidate lessons:

1. heating/cooling-load intuition;
2. vapor-compression refrigeration;
3. refrigerants and phase-change behavior;
4. heat pumps;
5. psychrometrics;
6. fans, ducts and pressure losses;
7. hydronic loops;
8. pumps, boilers and chillers;
9. ventilation and indoor-air quality;
10. controls architecture, with Controls handoff;
11. insulation and envelope interactions;
12. plumbing/mechanical-service basics;
13. commissioning and balancing;
14. common HVAC/refrigeration failure signatures;
15. cold-chain engineering;
16. resilient/off-grid thermal systems.

#### B-AERO-01 — Aerodynamics and gas dynamics

Candidate lessons:

1. aerodynamic forces and coefficients;
2. pressure, velocity and streamline interpretation;
3. airfoil lift;
4. circulation and lift intuition;
5. profile, induced and wave drag;
6. finite wings and aspect ratio;
7. boundary layers and skin friction;
8. separation and stall;
9. high-lift devices;
10. compressibility and Mach number;
11. normal/oblique shocks;
12. expansion waves;
13. transonic flow;
14. supersonic flow;
15. hypersonic flow;
16. aerothermodynamics;
17. aeroelasticity and flutter awareness;
18. propeller/rotor aerodynamics;
19. wind-tunnel and CFD interpretation;
20. handoff to Flight Dynamics.

#### B-AERO-02 — Propulsion, turbomachinery and combustion systems

Candidate lessons:

1. thrust from momentum change;
2. propeller and fan propulsion;
3. turbomachinery energy transfer;
4. compressor behavior;
5. turbine behavior;
6. compressor/turbine maps, choke and surge;
7. practical Brayton-cycle engines;
8. turbojets and turbofans;
9. ramjets/scramjets awareness;
10. nozzle flow;
11. rocket equation and staging intuition;
12. liquid-rocket systems;
13. solid/hybrid-rocket awareness;
14. flame structure and combustion chemistry;
15. ignition, stability and emissions;
16. reciprocating-engine fundamentals;
17. pumps and compressors;
18. electric propulsion;
19. efficiency, thermal limits and cooling;
20. propulsion-system matching.

#### B-SPACE-01 — Space systems and astrodynamics awareness

Candidate lessons:

1. orbital elements and orbit geometry;
2. two-body orbital motion;
3. orbit energy and period;
4. maneuvers and delta-v;
5. transfer orbits;
6. perturbations and station keeping;
7. launch and ascent architecture;
8. spacecraft attitude dynamics, with Controls/GNC handoff;
9. structures and mechanisms;
10. spacecraft thermal control;
11. electrical power generation/storage;
12. communications, with RF handoff;
13. avionics and onboard computing;
14. space propulsion;
15. radiation, vacuum and charging environment;
16. mission design and operations;
17. rendezvous/docking awareness;
18. entry, descent and landing;
19. ground systems;
20. space-system trade studies.

### Electrical, computer and computational breadth

#### B-EE-01 — Circuit theory and practical electricity

Candidate lessons:

1. charge, current, voltage and power;
2. resistance and Ohm's law;
3. KCL and KVL;
4. series/parallel networks;
5. source models;
6. Thevenin and Norton equivalents;
7. capacitors;
8. inductors;
9. first-order transients;
10. second-order RLC behavior;
11. AC sinusoids and phasors;
12. impedance;
13. resonance;
14. real/reactive/apparent power;
15. three-phase basics;
16. filters and frequency response;
17. transformers;
18. grounding, protection and safe measurement;
19. practical wiring/load calculations;
20. handoff to analog, power and RF courses.

#### B-EE-02 — Analog electronics

Candidate lessons:

1. diode behavior and rectification;
2. BJTs;
3. MOSFETs;
4. biasing and operating points;
5. small-signal gain;
6. op-amp ideal model;
7. practical op-amp limitations;
8. feedback;
9. active filters;
10. comparators and Schmitt triggers;
11. oscillators;
12. linear regulators and references;
13. analog interfaces to ADCs/DACs;
14. instrumentation amplifiers;
15. noise and signal-to-noise;
16. sensor front ends;
17. protection, ESD and fault containment;
18. PCB parasitics, grounding and analog debugging.

#### B-EE-03 — Digital electronics and computer hardware

Candidate lessons:

1. binary representation and logic levels;
2. Boolean gates;
3. combinational logic;
4. sequential logic;
5. clocks, setup/hold and metastability;
6. finite-state machines;
7. counters and timers;
8. buses and handshaking;
9. memory technologies;
10. processor datapaths;
11. caches and memory hierarchy;
12. interrupts and DMA;
13. common serial interfaces;
14. digital signaling and signal-integrity awareness;
15. ADC/DAC digital interfaces;
16. microarchitecture concepts;
17. hardware debugging;
18. handoff to FPGA Data Path and Embedded RT/HIL.

#### B-EE-04 — Power electronics, electric machines and drives

Candidate lessons:

1. semiconductor switching devices;
2. switching losses and thermal limits;
3. PWM;
4. rectifiers;
5. buck converters;
6. boost and buck-boost converters;
7. isolated converter concepts;
8. inverters;
9. magnetics and transformers in converters;
10. gate drives and protection;
11. DC motors;
12. BLDC/PMSM machines;
13. induction machines;
14. generators;
15. torque-speed curves;
16. regenerative operation;
17. motor drives and field-oriented-control concepts;
18. EMI/power-quality awareness;
19. machine/converter sizing;
20. fault and thermal signatures.

#### B-EE-05 — Power systems, grids and microgrids

Candidate lessons:

1. how electrical grids are organized;
2. generation types and prime movers;
3. three-phase power;
4. transformers and substations;
5. transmission lines;
6. distribution systems;
7. per-unit reasoning conceptually;
8. real/reactive power flow;
9. voltage regulation;
10. frequency balance;
11. fault current;
12. breakers, relays and protection zones;
13. grounding and earthing;
14. stability concepts;
15. renewable generation integration;
16. inverter-based resources;
17. battery/storage integration;
18. microgrids and islanding;
19. black-start/resilience concepts;
20. electrical safety and operational boundaries.

#### B-EE-06 — Sensors, instrumentation and measurement science

Candidate lessons:

1. the measurement chain;
2. standards, traceability and calibration;
3. accuracy, precision, resolution and uncertainty;
4. loading and nonideal measurement effects;
5. temperature sensors;
6. strain, force and torque measurement;
7. pressure and flow measurement;
8. accelerometers and vibration sensors;
9. gyroscopes and IMUs;
10. magnetometers;
11. position, proximity and displacement sensors;
12. optical sensors;
13. microphones and acoustic sensors;
14. chemical and biosensors;
15. bridges and signal conditioning;
16. ADC/DAQ architecture;
17. grounding, shielding and isolation;
18. calibration experiments and choosing the next measurement;
19. handoff to Stats/Estimation;
20. handoff to HWIL/Test Systems.

#### B-COMP-01 — Computer systems, networking and software foundations for engineers

Candidate lessons:

1. binary data representation;
2. CPU, memory and storage hierarchy;
3. operating-system processes and threads;
4. filesystems and persistence;
5. concurrency and race-condition awareness;
6. networking layers and packet flow;
7. IP, routing and transport concepts;
8. local/industrial serial and network interfaces;
9. distributed-system concepts;
10. databases and data models;
11. algorithms and data-structure literacy;
12. compiler/build/toolchain concepts;
13. scripting and automation;
14. software architecture and interfaces;
15. testing and version control;
16. cybersecurity fundamentals;
17. cryptography concepts;
18. containers/cloud deployment concepts;
19. CPU/GPU/HPC awareness;
20. handoff to Distributed Real-Time and Embedded RT/HIL.

#### B-AI-01 — Artificial intelligence, machine learning and computational intelligence

Candidate lessons:

1. what constitutes a learning problem;
2. datasets, features and labels;
3. regression;
4. classification;
5. trees and ensembles;
6. clustering;
7. dimensionality reduction;
8. neural-network fundamentals;
9. deep learning;
10. convolutional vision systems;
11. sequence models and language-model concepts;
12. probabilistic/Bayesian learning;
13. reinforcement learning;
14. fuzzy logic;
15. evolutionary and swarm computation;
16. evaluation, overfitting and distribution shift;
17. uncertainty and failure modes;
18. physics-informed/hybrid modeling;
19. deployment, compute and data constraints;
20. handoff to domain-specific autonomy/control work.

### Materials, chemistry, process and energy breadth

#### B-MAT-01 — Materials science and engineering

Candidate lessons:

1. atomic bonding and material families;
2. crystal structures;
3. defects and dislocations;
4. diffusion;
5. phase diagrams;
6. phase transformations;
7. strengthening mechanisms;
8. stress-strain behavior;
9. steels and ferrous alloys;
10. aluminum, titanium and nonferrous alloys;
11. heat treatment;
12. ceramics and glass;
13. polymers and elastomers;
14. fiber/particle composites;
15. semiconductor/electronic materials;
16. magnetic, optical and smart materials;
17. corrosion and oxidation;
18. fracture;
19. fatigue and creep;
20. material selection, processing and failure signatures.

#### B-CHEM-01 — Chemistry for engineers

Candidate lessons:

1. atomic structure and periodic trends;
2. chemical bonding;
3. molecular shape and intermolecular forces;
4. moles and stoichiometry;
5. gases;
6. liquids, solids and solutions;
7. thermochemistry;
8. entropy and free energy;
9. chemical equilibrium;
10. acids and bases;
11. oxidation/reduction;
12. chemical kinetics;
13. catalysis;
14. organic functional groups;
15. polymer chemistry;
16. surface and colloid chemistry;
17. analytical/measurement chemistry;
18. chemical compatibility and safety reasoning.

#### B-CHE-01 — Chemical and process engineering

Candidate lessons:

1. process-flow diagrams and unit operations;
2. material balances;
3. energy balances;
4. fluid transport;
5. heat transport;
6. mass transport;
7. chemical kinetics;
8. batch and continuous reactors;
9. reactor residence time and conversion;
10. distillation;
11. absorption and stripping;
12. liquid-liquid extraction;
13. adsorption;
14. membranes;
15. crystallization, drying and solids handling;
16. catalysis and reactor/process coupling;
17. process control handoff;
18. process safety and scale-up;
19. flowsheet integration;
20. process economics and resource efficiency.

#### B-ELECTRO-01 — Electrochemistry, batteries, fuel cells and corrosion

Candidate lessons:

1. electrochemical potential;
2. Nernst-equation intuition;
3. electrode reactions;
4. charge-transfer kinetics;
5. ion transport and diffusion;
6. double layers and capacitance;
7. galvanic/electrolytic cells;
8. lead-acid and nickel systems;
9. lithium-ion cell architecture;
10. LFP/NMC and chemistry tradeoffs;
11. state-of-charge/state-of-health concepts;
12. degradation and thermal-runaway awareness;
13. charging constraints;
14. battery-pack architecture and BMS handoff;
15. fuel cells;
16. electrolysis and hydrogen;
17. supercapacitors;
18. corrosion and cathodic/protective methods.

#### B-ENERGY-01 — Energy systems, conversion, storage and resilience

Candidate lessons:

1. energy versus power and system boundaries;
2. efficiency, exergy and losses;
3. fossil/thermal generation;
4. hydropower;
5. wind energy;
6. solar photovoltaics;
7. solar thermal;
8. geothermal energy;
9. biomass and waste-to-energy;
10. nuclear-energy handoff;
11. electrochemical storage;
12. mechanical and thermal storage;
13. hydrogen and synthetic fuels;
14. heat pumps and electrified heat;
15. combined heat and power;
16. grid-interface handoff;
17. lifecycle/resource constraints;
18. energy economics at a conceptual level;
19. microgrids and resilience;
20. integrated energy-budget capstone.

#### B-NUC-01 — Nuclear engineering

Candidate lessons:

1. neutron interactions and cross-section intuition;
2. fission chains and neutron economy;
3. multiplication and criticality concepts;
4. moderators, reflectors and absorbers;
5. reactor cores and common reactor types;
6. reactor thermal hydraulics;
7. fuel and cladding;
8. decay heat;
9. reactor kinetics/control concepts;
10. shielding;
11. radiation protection;
12. defense in depth and engineered safety systems;
13. nuclear materials and degradation;
14. fuel cycle and waste;
15. fusion-engineering concepts;
16. non-power nuclear applications and instrumentation.

### Civil, infrastructure, environment, marine and resource breadth

#### B-CIV-01 — Civil and structural engineering

Candidate lessons:

1. civil loads and load combinations;
2. structural load paths;
3. structural system selection;
4. trusses, frames and lateral systems;
5. beams and columns at building scale;
6. reinforced concrete;
7. prestressed concrete;
8. structural steel;
9. timber and masonry;
10. connections and detailing concepts;
11. foundations interface;
12. wind loading;
13. earthquake engineering;
14. structural dynamics;
15. bridges;
16. building structures;
17. inspection, distress and damage recognition;
18. temporary works;
19. repair and retrofit;
20. codes, safety factors and professional boundaries.

#### B-CIV-02 — Geotechnical and geological engineering

Candidate lessons:

1. engineering geology and the rock cycle;
2. soil classification;
3. three-phase soil relations;
4. effective stress;
5. permeability and seepage;
6. consolidation and settlement;
7. compaction;
8. shear strength;
9. bearing capacity;
10. shallow foundations;
11. deep foundations;
12. retaining structures;
13. slope stability;
14. rock mechanics;
15. excavation and tunneling;
16. liquefaction;
17. site investigation;
18. engineering geophysics and ground-risk communication.

#### B-CIV-03 — Hydraulics, hydrology and water resources

Candidate lessons:

1. the hydrologic cycle;
2. rainfall and runoff;
3. watersheds and hydrographs;
4. frequency/risk concepts with Stats handoff;
5. open-channel flow;
6. pipe flow;
7. pumps and pumping stations;
8. pipe networks;
9. reservoirs and dams;
10. groundwater;
11. wells and aquifers;
12. urban drainage and stormwater;
13. flood routing and floodplain thinking;
14. erosion and sediment transport;
15. irrigation and drainage;
16. municipal water-supply systems;
17. hydraulic structures;
18. water-energy and drought/resilience tradeoffs.

#### B-CIV-04 — Transportation, surveying, construction and municipal systems

Candidate lessons:

1. surveying coordinates, leveling and error;
2. GNSS/GIS concepts;
3. roadway geometric design;
4. pavement behavior;
5. traffic flow;
6. intersections and signal-control concepts;
7. rail systems;
8. airport/airfield infrastructure;
9. ports and intermodal freight interfaces;
10. earthwork and grading;
11. construction methods and sequencing;
12. construction equipment;
13. scheduling and critical-path concepts;
14. cost estimating;
15. temporary works and jobsite logistics;
16. utility coordination;
17. municipal infrastructure interfaces;
18. inspection, maintenance and asset management;
19. codes/permitting concepts;
20. emergency access and resilient transportation.

#### B-ENV-01 — Environmental engineering

Candidate lessons:

1. environmental mass balances;
2. water-quality parameters;
3. drinking-water treatment trains;
4. coagulation, filtration and disinfection;
5. wastewater collection;
6. primary/secondary/tertiary treatment;
7. biological treatment;
8. sludge and residuals;
9. air pollutants and atmospheric dispersion concepts;
10. air-pollution control;
11. solid-waste systems;
12. hazardous-waste handling concepts;
13. contaminated soil and groundwater;
14. remediation technologies;
15. contaminant fate and transport;
16. environmental chemistry;
17. environmental monitoring and sampling;
18. risk assessment;
19. sustainability/lifecycle assessment;
20. resource recovery and climate adaptation.

#### B-MAR-01 — Ocean, marine and naval engineering

Purpose: provide the exact kind of "load up marine engineering and understand ship dynamics in several pages plus interactions" experience that motivates this breadth layer.

Candidate lessons:

1. the seawater environment and marine design drivers;
2. hydrostatics and buoyancy;
3. displacement, draft and trim;
4. intact stability and metacentric height;
5. hull forms and principal dimensions;
6. resistance and drag;
7. marine propulsion;
8. propellers and cavitation;
9. six-degree-of-freedom ship dynamics;
10. seakeeping, heave/pitch/roll and encounter frequency;
11. maneuvering and control, with Controls handoff;
12. waves and wave loading;
13. marine structures and fatigue;
14. offshore platforms, moorings and station keeping;
15. marine corrosion and materials;
16. shipboard power, pumps and auxiliary systems;
17. underwater acoustics, with DSP handoff;
18. AUV/ROV systems, with Robotics handoff;
19. damage stability and flooding awareness;
20. naval-architecture trade studies.

Representative interactions: hull loading/buoyancy geometry, center-of-gravity/metacentric-height stability sandbox, roll resonance versus wave encounter, propeller cavitation region, simplified flooding/damage-stability comparison.

#### B-RES-01 — Mining, petroleum and subsurface resource engineering

Candidate lessons:

1. resource geology and exploration;
2. orebody and reservoir characterization;
3. surface-mining concepts;
4. underground-mining concepts;
5. rock breakage and excavation awareness;
6. mine ventilation and material transport;
7. mineral processing and separation;
8. drilling fundamentals;
9. well construction and integrity;
10. reservoir porosity and permeability;
11. subsurface pressure and flow;
12. multiphase production;
13. artificial-lift concepts;
14. reservoir management;
15. enhanced-recovery concepts;
16. tailings, produced water and environmental constraints;
17. geomechanics and subsidence;
18. closure, remediation, resource economics and depletion.

#### B-AG-01 — Agricultural, food and biological-systems engineering

Candidate lessons:

1. soils and root-zone water;
2. irrigation;
3. drainage;
4. pumps and farm water systems;
5. tractors and mobile power;
6. field machinery and mechanisms;
7. precision agriculture, sensing and GNSS;
8. greenhouses and controlled environments;
9. agricultural HVAC/energy;
10. harvesting and post-harvest handling;
11. grain storage and drying;
12. refrigeration and cold chain;
13. food-process unit operations;
14. sanitation and food-safety systems;
15. livestock-facility systems;
16. anaerobic digestion;
17. biomass/bioenergy;
18. nutrient, water and waste recycling;
19. resilient/local food-system design;
20. biological-process handoff to chemical/biomedical courses.

### Biomedical, industrial, systems, human and safety breadth

#### B-BME-01 — Biomedical engineering

Candidate lessons:

1. physiology as interacting engineered systems;
2. biomechanics;
3. bioelectric potentials;
4. bioinstrumentation;
5. biosensors;
6. ECG/EEG/EMG signal concepts, with DSP handoff;
7. X-ray imaging;
8. CT;
9. MRI;
10. ultrasound imaging;
11. biomaterials;
12. prosthetics and orthotics;
13. rehabilitation engineering;
14. neural engineering;
15. tissue engineering;
16. microfluidics/lab-on-chip;
17. drug-delivery/device interfaces;
18. sterilization and biocompatibility;
19. medical-device safety/regulatory concepts;
20. human factors and clinical-system constraints.

#### B-IE-01 — Industrial engineering, operations, logistics and quality

Candidate lessons:

1. process mapping;
2. throughput, cycle time and work in process;
3. bottlenecks and Little's Law;
4. queueing in operations;
5. capacity planning;
6. scheduling;
7. inventory systems;
8. forecasting, with Stats handoff;
9. supply chains;
10. logistics and transportation networks;
11. facility layout;
12. lean systems;
13. statistical process control, with Stats handoff;
14. quality systems and root-cause thinking;
15. operations research framing;
16. optimization handoff;
17. decision analysis;
18. ergonomics/human factors;
19. reliability/maintainability handoff;
20. lifecycle cost and operational resilience.

#### B-SE-01 — Systems engineering, architecture and technical decision-making

Candidate lessons:

1. mission, context and stakeholder framing;
2. problem statements and need identification;
3. requirements;
4. measures of effectiveness and performance;
5. functional decomposition;
6. physical/logical architecture;
7. interfaces and interface control;
8. mass/power/data/thermal/resource budgets;
9. trade studies;
10. modeling and abstraction;
11. model-based systems engineering concepts;
12. uncertainty and risk;
13. hazards and safety;
14. reliability/FDIR handoff;
15. verification versus validation;
16. integration strategy;
17. configuration/change management;
18. lifecycle, sustainment and obsolescence;
19. system-of-systems thinking;
20. technical reviews, evidence and decision records;
21. engineering ethics and communicating uncertainty;
22. HIL/HWIL handoff to the existing depth tracks.

#### B-HF-01 — Human factors, ergonomics and cognitive systems engineering

Candidate lessons:

1. human sensory capabilities and limitations;
2. perception and signal detection;
3. attention and workload;
4. memory and decision making;
5. situation awareness;
6. display design;
7. control/interface design;
8. alarms and alerting;
9. procedures and checklists;
10. human error and error-tolerant design;
11. anthropometry and physical ergonomics;
12. automation trust and mode awareness;
13. team/crew coordination;
14. usability testing and representative-user evidence;
15. safety culture and organizational contributors;
16. human-machine handoffs in high-consequence systems.

#### B-SAFE-01 — Safety, fire and process-hazard engineering

Candidate lessons:

1. hazard versus risk;
2. stored energy and hazardous-energy recognition;
3. hierarchy of controls and safe isolation;
4. hazard analysis;
5. FMEA/FTA concepts, with Reliability handoff;
6. HAZOP concepts;
7. pressure-system hazards;
8. thermal hazards;
9. electrical hazards;
10. chemical compatibility and exposure;
11. combustion and fire behavior;
12. fire detection and suppression;
13. egress and life safety;
14. explosion/overpressure awareness;
15. machine guarding and mechanical hazards;
16. process-safety layers;
17. incident investigation;
18. emergency systems, resilience and professional boundaries.

### Cross-disciplinary synthesis

#### B-FIELD-01 — Field engineering and resilient-system diagnosis

Purpose: turn the survey knowledge into a systems-engineering habit. This course is explicitly about diagnosis, safe restoration and reasoning across subsystem boundaries rather than specialist design certification.

Candidate lessons:

1. rapidly mapping an unfamiliar system;
2. identifying hazards, energy sources and safe isolation points;
3. deciding what to measure before touching anything;
4. using conservation laws and budgets to localize faults;
5. electrical source/load/distribution triage;
6. generators, batteries and microgrid restoration concepts;
7. water source, pumping, storage and distribution triage;
8. basic water-treatment train reasoning;
9. structural/shelter damage triage and load-path awareness;
10. HVAC, refrigeration and cold-chain diagnosis;
11. bearings, shafts, belts, gears and mechanical-drive diagnosis;
12. pipe, valve, pump, leak and cavitation diagnosis;
13. combustion/engine and thermal-system fault signatures;
14. sensors, calibration and instrumentation under degraded conditions;
15. communications/RF handoff and basic system-interface reasoning;
16. choosing substitute materials, fasteners and repair processes;
17. sanitation, waste and environmental-control systems;
18. biomedical/medical-equipment support boundaries;
19. logistics, spares, maintenance prioritization and cannibalization tradeoffs;
20. fault trees, uncertainty and stop/go decisions;
21. resource-constrained system redesign;
22. integrated remote-facility capstone: restore power, water, thermal control, communications and critical loads with incomplete information.

### Explicit depth-owned topics: no duplicate breadth course

The following taxonomy items are intentionally NOT assigned a new standalone breadth course because the existing platform already owns or reserves deeper treatment. They should appear as prerequisites, bridge lessons or handoff links only:

- classical/modern/robust/adaptive/nonlinear/digital/optimal/MPC/stochastic/distributed/fuzzy control;
- guidance, navigation, state estimation, Kalman filtering and sensor fusion;
- DSP, statistical signal processing, image/audio/speech processing and array processing;
- radar, tracking, SAR, phased arrays and radar signal processing;
- RF/microwave/mmWave, transmission lines, S-parameters, matching, antennas and applied RF measurement;
- communications theory, modulation, coding and wireless systems;
- robotics kinematics/dynamics, planning, SLAM, perception, autonomy and multi-agent robotics;
- flight dynamics, aircraft stability/control and detailed aircraft performance;
- vehicle dynamics, tires, chassis, propulsion/telemetry and vehicle controls;
- numerical optimization, mathematical programming and optimal numerical methods;
- statistics, statistical inference, Bayesian estimation, time series and dedicated estimation theory;
- reliability engineering, maintainability, FDIR, formal failure analysis and reliability evidence;
- FPGA/HDL implementation and data-path design;
- embedded real-time implementation, RTOS behavior and real-time HIL;
- distributed real-time systems;
- HWIL architecture, automated test systems and deep verification/test execution.

Breadth lessons may use examples from these areas, but implementation MUST link to the owning depth curriculum rather than clone it.

### Coverage map for the original discipline taxonomy

The breadth curriculum plus the depth-owned tracks above is intended to cover the complete mathematics/physics/engineering taxonomy represented in this roadmap expansion:

- mathematics: algebra, geometry, trigonometry, calculus, linear algebra, ODEs, PDEs, vector calculus, analysis, algebraic structures, geometry/topology, discrete math, applied math, dynamical systems and numerical methods;
- probability/statistics/estimation and optimization: depth-owned, with prerequisite-level bridges from mathematics;
- classical/solid/continuum mechanics: B-PHYS-01, B-MECH-01 and B-MECH-02;
- fluids, aero and gas dynamics: B-MECH-05 and B-AERO-01;
- thermodynamics, heat/mass transfer and combustion: B-MECH-03, B-MECH-04 and B-AERO-02;
- waves/acoustics: B-PHYS-02;
- electromagnetism: B-PHYS-03;
- optics/photonics: B-PHYS-04;
- quantum/AMO: B-PHYS-05;
- condensed matter/solid-state: B-PHYS-06;
- nuclear/particle/radiation: B-PHYS-07 and B-NUC-01;
- relativity/gravitation/cosmology: B-PHYS-08;
- plasma/MHD: B-PHYS-09;
- geophysics, atmosphere, ocean and space environment: B-PHYS-10;
- circuit/electronics/power engineering: B-EE-01 through B-EE-05;
- sensors/instrumentation: B-EE-06;
- computer engineering/computational systems: B-COMP-01 plus FPGA/embedded/distributed depth tracks;
- AI/computational intelligence: B-AI-01;
- mechanical design/manufacturing/HVAC: B-MECH-06 through B-MECH-08;
- aerospace: B-AERO-01, B-AERO-02, B-SPACE-01 plus Flight Dynamics depth;
- materials: B-MAT-01;
- chemistry/chemical engineering/electrochemistry: B-CHEM-01, B-CHE-01 and B-ELECTRO-01;
- energy engineering: B-ENERGY-01;
- civil/structural/geotechnical/water/transport/construction: B-CIV-01 through B-CIV-04;
- environmental engineering: B-ENV-01;
- marine/ocean/naval engineering: B-MAR-01;
- petroleum/mining/resource engineering: B-RES-01;
- agricultural/food/biological systems: B-AG-01;
- biomedical engineering: B-BME-01;
- industrial/operations engineering: B-IE-01;
- systems engineering: B-SE-01;
- human factors: B-HF-01;
- safety/fire/process-hazard engineering: B-SAFE-01;
- controls, GNC, robotics, DSP/radar, RF, flight dynamics, vehicle dynamics, numerical optimization, statistics/estimation, reliability/FDIR, FPGA, embedded/distributed real time and HWIL/test: existing depth-owned curricula.

### Suggested prerequisite topology

The breadth layer should be navigable without forcing a four-year linear degree plan.

Foundation nodes:

- B-MATH-01 before essentially every quantitative course;
- B-MATH-02 before courses that rely heavily on fields, dynamics, transport or waves;
- B-MATH-03 before advanced mechanics, quantum, computer hardware or state-space-heavy bridges;
- B-CHEM-01 before materials, chemical/process, electrochemistry and environmental chemistry.

Natural clusters:

- mechanics cluster: B-PHYS-01 -> B-MECH-01/B-MECH-02 -> B-MECH-06 -> discipline applications;
- thermal/fluids cluster: B-MECH-03 -> B-MECH-04/B-MECH-05 -> HVAC, aero, propulsion, chemical, energy, marine and water;
- E&M cluster: B-PHYS-03 -> B-EE-01 -> analog/digital/power/sensors, with RF depth as a branch;
- modern-physics cluster: B-PHYS-03/B-PHYS-05 -> optics, condensed matter, nuclear and plasma;
- infrastructure cluster: statics + fluids + thermodynamics + materials -> civil/environmental/marine/agriculture;
- systems cluster: B-SE-01 can be taken early, but B-FIELD-01 should sit after a representative set of mechanical, electrical, thermal, materials, civil/water and systems courses.

No learner should be blocked from sampling a topic because a prerequisite is incomplete; prerequisites are recommendations and the UI should permit "just-in-time prerequisite" links.

### Breadth assessments

Breadth assessments should avoid traditional multi-page calculation exams. Preferred tasks:

- identify the governing conservation law;
- choose which of several models is valid;
- predict a trend before moving a slider;
- read a graph and explain a regime change;
- estimate an order of magnitude;
- detect a unit or scale error;
- identify which assumption failed;
- choose the next useful measurement;
- rank likely failure causes;
- draw or complete a subsystem/interface diagram;
- explain what additional specialist evidence is required;
- complete one course-level diagnostic or design-trade mini-capstone.

A cumulative generalist assessment should present an unfamiliar engineered system and ask the learner to decompose it across disciplines, establish energy/material/information flows, identify hazards and interfaces, propose measurements, isolate likely faults and explicitly call out where specialist depth is needed.

### Implementation strategy after explicit future authorization

This roadmap entry does not authorize implementation. When the owner chooses to activate the breadth program:

1. create one Portfolio Control umbrella milestone for the breadth layer without disturbing the existing depth-course roadmaps;
2. build a machine-readable taxonomy/coverage matrix mapping every named discipline to either one breadth course or one existing depth owner;
3. author competency maps before lesson counts are frozen;
4. pilot three materially different survey courses:
   - B-MAR-01 Ocean, Marine and Naval Engineering, because it exercises geometry, fluids, structures, waves, dynamics and systems;
   - B-PHYS-04 Optics and Photonics, because it exercises fields, wave visualizations and imaging;
   - B-CIV-03 Hydraulics, Hydrology and Water Resources, because it exercises infrastructure, network flow, storage and real-world diagnostic reasoning;
5. use those pilots to tune lesson length, optional-math presentation and breadth-assessment semantics;
6. implement remaining courses in coherent prerequisite groups, with no more than ten new lessons per authorized batch under the Course Caliber rule;
7. require explicit depth-track handoff links anywhere the breadth layer touches a reserved domain;
8. maintain a global coverage dashboard distinguishing:
   - taxonomy mapped;
   - competency map reviewed;
   - lessons authored;
   - interactive content implemented;
   - numerical/physical models verified;
   - cumulative breadth assessment present;
   - representative learner validation;
9. add the B-FIELD-01 synthesis course only after enough mechanical, electrical, thermal, infrastructure, materials and systems breadth exists to make it genuinely cross-disciplinary.

### Success criterion

The breadth program is complete only when the taxonomy coverage matrix shows every intended mathematics, physics and engineering discipline either:

- covered by a reviewed breadth course at the recognition/reasoning level; or
- explicitly owned by an existing depth curriculum with a working handoff.

The desired learner outcome is not "I can derive every equation." Nor is breadth-course completion intended to certify professional design competence. The product-level pacing target is that a motivated learner can complete roughly one breadth course per weekend and traverse the full 56-course breadth map in about a year, give or take.

The desired outcome is:

> I can look at an unfamiliar engineered system, recognize the physics and disciplines involved, reason about the dominant quantities and constraints, ask useful questions, make defensible first-order estimates, interpret evidence, avoid obvious category errors, and know what depth is required next.

That is the breadth standard for the platform's generalist / systems-engineer track.
