# Revised-course quality audit — 2026-09-28

The four revised engineering curricula are embedded as 288 native interactive
lessons, alongside two example lessons. Thirteen source repositories are pinned;
nine remain source-only. Source presence is not native browser delivery.

| Curriculum | Native lessons | Content position |
| --- | ---: | --- |
| DSP and Radar | 84 | P01–P84 item-level fidelity repairs retained; aggregate competency and cumulative-assessment review pending |
| Controls and GNC | 68 | Prior artifacts retained; final capstone cumulative claims reopened |
| Robotics and Autonomy | 69 | Prior artifacts retained; final capstone cumulative claims reopened |
| Vehicle Dynamics | 67 | P66/P67 cumulative models fail direct semantic inspection; aggregate numerical, curriculum and capstone claims reopened |

## Confirmed content defects and next repair

Vehicle **P66** sets nine subsystem flags to one and flips fixed entries in broken
mode. Its held-out residual is an algebraic surrogate; it does not execute the
provenance, alignment, calibration, reconstruction and identification chain named
in `requirements-trace.yaml`.

Vehicle **P67** computes `lap = 92 - 20 * setup_delta` and sets eleven subsystem
flags directly. It does not integrate the tire, chassis, propulsion, brakes,
aero, track, line and uncertainty models claimed in its requirements trace.
Its design signature also declares dimensionless units for time-valued metrics.
Independent code that reproduces a surrogate does not establish the missing
integration. Passing existing tests did not detect this error.

Both defects are displayed with the affected lesson in the browser. A separate
scoped content batch must replace these surrogates with executed cumulative
models, independently assess their physical invariants and failure/recovery,
and review the neighboring performance prerequisites. No course payload is
changed in the delivery batch.

The next coherent revision group contains exactly twelve existing lessons:
Controls P66–P68, Robotics P68–P69, and Vehicle P61–P67. Controls uses algebraic
tracking/NEES, survey error and latency/drop surrogates in place of the claimed
closed-loop capstones. Robotics executes planning/kinematics/contact models but
sets some replay/recovery verdicts from the failure switch. Vehicle P61–P65
also need dimensional signature corrections and specific limiting cases; P64
caps reported energy without coupling the budget into the speed solution and
adds an artificial offset to its braking violation metric.

These findings reopen the aggregate numerical, curriculum and capstone statuses
of all three courses. DSP remains blocked on its already planned aggregate
mapping and assessment review. The repair scope adds no new lessons.

## Wider review: additional blocked lessons

Further direct inspection found **44 additional issues**, making **56 affected
lessons** in the current register. Controls has 22 affected lessons, Robotics 27,
and Vehicle seven. The initially selected twelve remain a separate repair group;
they no longer represent the complete defect backlog. See the
[additional finding register](course-quality/additional-semantic-findings.md)
for each exact lesson and mechanism. These findings are also attached to the
affected browser lessons. No unlisted lesson is automatically certified.

## Per-lesson evidence

- `course-quality/lesson-audit.json`: all 288 engineering lessons, payload hashes,
  concept headings, candidate equations/checks, control labels/units, declared
  predictions/plots/interpretations, evidence paths, map availability and named
  semantic defects. Presence findings are **not** pass certificates.
- `course-quality/browser-report.json`: actual Chromium desktop/mobile results,
  automated accessibility findings, rendered plots/metrics/math, page errors,
  overflow, representative interactions and screenshot hashes.
- `course-quality/container-report.json`: actual nonroot read-only container,
  every baked default via HTTP, deterministic repeats, digest rejection,
  declared broken-mode recovery, response sizes and deep/static routes.

The browser embeds the lesson-specific content review and known limitations.
Equations render through KaTeX; code/currency remain literal. Revision hashes
are in a collapsed technical disclosure. Navigation supports keyboard focus,
and plots expose numeric ranges in addition to the lesson's interpretation and
metrics. Numeric ranges are not a complete nonvisual description of a curve.

## Remaining acceptance boundaries

Automated accessibility checks and named agent screenshot inspection are
separate from manual screen-reader and representative-learner acceptance.
Those human studies have not run. MATLAB runtime, measured vehicle/track,
hardware/HIL, production deployment and the nine source-only conversions are
not claimed. The course inventory is not evidence of curriculum completeness.

Run `./scripts/verify-course-delivery.sh` with Node 22.12 or newer and a
fresh container name/localhost port. It builds the actual image, waits for
readiness, runs browser and HTTP checks, writes the reports and stops its own
container. The report records the image identity; no production service is
modified. Revert this isolated batch to roll back; no schema or data migration.

## Browser-only numeric boundary

Real browser requests exposed a separate platform defect: JavaScript serializes
`240.0` as `240`, while the old menu validator demanded the same Python scalar
type as the declared option. DSP P17–P20 could therefore pass Python HTTP tests
and still fail in the browser. Control amendment PR532 permits the narrow
repair: equal finite numeric spellings resolve to the declared option value;
booleans, strings and undeclared values remain distinct. Numerically duplicate
menu options are rejected at authoring time. No existing course manifest or
public schema shape changes. Regression checks cover the actual browser request.

The verification script installs the Chromium revision selected by the pinned
Playwright package. The host must supply Chromium's operating-system libraries;
this is development verification tooling, not a runtime container dependency.
Numeric alias rejection tightens authoring validation: remove duplicate `1`/`1.0`
choices from an ambiguous manifest. The audit found no such current manifests.
