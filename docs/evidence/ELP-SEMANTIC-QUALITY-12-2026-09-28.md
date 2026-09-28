# Twelve lesson semantic revision

Status: implementation and mandatory local/browser/container verification passed; merge tracked in CURRENT_STATE.md.

The batch starts from delivery PR52, commit
`4e8e39fb3fc05eef8b4ca5607bec4d0bc9320891`, tree
`51d97a215479ea8103decb5901592dac3dd3b98a`. Control PR534 activated the
twelve-lesson scope; control PR537, merged as
`74a44e66d9449e9b6e810051f806a4133be0202d`, added the demonstrated generic
2D rendering repair. Owner continuation retains explicit development merge
authorization. There is no production deployment.

## Implemented mechanisms and evidence

| Lessons | Executed revision | Independent check |
| --- | --- | --- |
| Controls P66 | Persistently excited calibration, fitted discrete plant, feedback and scalar Kalman estimation across three stressed plants; computed rank/tracking/command/NEES verdicts. | Explicit normal equations and information-form estimator; rank, state recurrence and parameter-corner checks. |
| Controls P67 | Exact planar arcs, timed GNSS/inertial observations, waypoint guidance, bounded turns and stale-data forward hold. | Complex-arc replay and geometric/timing checks. |
| Controls P68 | Delayed timestamped command arrivals, dropped burst, old-packet rejection, closed-loop plant and fail-zero watchdog. | Independently reconstructed arrivals and no-fault limits. |
| Robotics P68 | Observed occupancy, A* replanning, fresh-data resume and continuous segment separation against a moving obstacle. | Reverse breadth-first routing and independent relative-motion geometry. |
| Robotics P69 | Calibrated two-link reach, explicit static support model, delayed contact commands, timestamp guards and exact positive spring work. | Complex kinematics, independent arrival replay and trapezoidal force-work calculation. |
| Vehicle P61 | Corrected dimensional signatures and parameter-sample mean interpretation. | Independent ellipse geometry, circle/scaling limits and sample refinement. |
| Vehicle P62 | Corrected signature order/units; actual force-circle demand, drag and power limits. | Independent force balance and zero-speed limit. |
| Vehicle P63 | Closed parallel-curve candidates and local distance/speed time integral with dimensional offset penalty. | Independent scalar quadrature, circle and corridor limits. |
| Vehicle P64 | Cyclic speed reachability under tire/drive/brake forces; energy budget changes speed; braking work determines temperature. | Jacobi reachability, piecewise-linear energy solution, force/seam/refinement checks. |
| Vehicle P65 | Explicit synthetic factorial model with unused interior validation points and correctly signed time reductions. | Walsh/contrast solution, rank and disjoint validation points. |
| Vehicle P66 | Actual retained synthetic CAN/BLE fixture decoding/provenance, clock/sensor calibration, reconstruction, chronological identification and recovery. | Manual raw-byte decoding, scalar reconstruction, independent least squares and covariance/split checks. |
| Vehicle P67 | Explicit illustrative tire/load/gear/brake/aero/track/line/lap model, setup coupling, uncertainty endpoints and clean replay. | Scalar load/gear implementation with Gauss–Seidel reachability versus production Jacobi; conservation, force, refinement and limit checks. |

All twelve lessons include dimensioned relations, worked reasoning, predictions,
two sweeps, named faults and recovery, limiting cases and answer rationales.
Cumulative lessons expose verdicts computed from executed quantities in browser
tables. The UI describes these as scoped model reviews and keeps their limits
visible; it does not certify entire curricula.

The five retained scenarios per lesson produce **60 independent comparisons**.
Expected values originate solely in the separate reference implementation;
production values are executed through `ExperimentRuntime`. The new physical
and preservation suite passed **40 tests**, including 216 control-corner cases.
The reference preservation check retains unaffected function bytes and outputs.
See [semantic-revision.json](../course-quality/semantic-revision.json).

## Rendering finding and correction

Direct screenshots of the first container showed WebGL unsupported notices in
place of curves. A single existing Controls P01 page reproduced the problem
without simultaneous tabs. The earlier phrase/visibility check before interaction missed notices visible
in the screenshots, so a Plotly container and axes were insufficient evidence.
The negative screenshot and observation are retained in
[rendering-observation.json](../course-quality/rendering-observation.json).

The twelve bounded revised line plots use SVG. The generic renderer also
preserves coordinates/styles and selects SVG for existing 2D `scattergl` traces
when WebGL is unavailable. A successful context probe is insufficient: the
renderer also detects Plotly initialization notices or exceptions and retries
in SVG. It does not project 3D data or modify course
calculations. A disabled-WebGL browser test compares rendered coordinates with
the actual API response. The all-page driver now detects any WebGL notice and
requires actual revised curves after failure/recovery/reset. Horizontal legends
receive a separate bottom band, and top axes reserve space beneath chart titles;
the real browser regression asserts nonoverlapping label bounds.

## Verification

Final image: `sha256:a36d1113b784f73f9b3c9f957f97d7403ec3cfebdab368022b9957f5e5356b1b`. Local read-only nonroot preview: `http://127.0.0.1:8770`.

| Gate | Result |
| --- | --- |
| Control-plane validation for PR534 and PR537 | Passed. |
| Independent five-scenario comparisons | 60 passed. |
| Physical invariants and unaffected-reference preservation | 40 passed in 24.30 s before rendering-only changes; covered again by the final suite. |
| `agent-verify.sh contract` | 103 passed in 124.81s (0:02:04). |
| `agent-verify.sh quick` | 1305 passed, 3 warnings in 1358.60s (0:22:38). |
| `agent-verify.sh full` / `verify.sh` | 1305 passed, 3 warnings in 1216.05s (0:20:16); catalog/schema/compile/type/build passed. |
| Frontend tests | 10 passed in the final container verifier. |
| Focused browser regressions | 14 passed, including unavailable-WebGL and chart-initialization fallback. |
| Container HTTP checks | 290/290 passed, including repeat/recovery and static serving. |
| Desktop/mobile page and revised interactions | 580 final page identities verified: 579 initial passes plus one retained deadline failure resolved by six isolated same-image checks; 36 interactions passed; 24 interactions cover all twelve revised lessons on both viewports with actual drawn SVG plots. |
| Screenshot/content-digest reconciliation and visual review | 36 sweep plus nine focused visual screenshots hash-checked; all 290 content identities match both viewport rows. Focused visual review covers drawn curves/units and scrollable mobile requirement verdicts. |
| Scope, source-pin and whitespace review | Passed; semantic-scope-review.json retains paths and all thirteen source pins. |

The first broader expansion run had two failures: a substantive lesson-section
depth requirement, corrected with authored Robotics content, and a correct
stale-content rejection while a lesson was being edited during a live catalog
test. Both targeted reruns passed after source edits stopped. The first browser
sweep was rejected after visual inspection exposed blank WebGL charts; it is
not final acceptance evidence. No numerical oracle or source-identity check was
weakened to accommodate these failures.

Hosted CI is separately reported and is nonmandatory under retained owner
direction. Earlier delivery heads had missing pinned DSP source checkout and
shallow-history failures; local mandatory checks still apply. No claim of a
green current hosted run is made without its actual result.

## Limits, remaining work and rollback

Sixty additional findings remain blocked: Controls 19, Robotics 25 and Vehicle
16. None of those curricula receives aggregate maturity promotion from these
twelve repairs. DSP's competency map and cumulative assessment remain the next
separate authorized batch. The catalog remains six courses and 290 interactive
modules, of which 288 are engineering lessons in the four revised curricula.
Nine other source repositories remain source-only.

The models retain explicit approximation boundaries: deterministic NEES is not
statistical coverage, a timed software loop is not physical HIL, static friction
support is not full wrench closure, and the GR86-sized model is illustrative
rather than measured vehicle calibration. Human learning, manual screen-reader,
MATLAB execution, measured vehicle/hardware and production validation are
`not_run`.

The earlier six-page, two-CPU deadline failure remains recorded. Final browser
checks pace real experiment requests one at a time without mocking responses;
they do not certify concurrent-user capacity.

Rollback is a revert of this isolated revision to PR52, retaining the honest
defect register. No schema migration, learner data or source-pin change occurs.

The final current reports include the rendering correction. Earlier delivery DOM checks
remain historical evidence of their named assertions and did not establish that
every WebGL curve was drawn. The negative result and correction are retained.

A completed 580-row pre-spacing sweep retained all passing rows but its process
ended with signal 143 during finalization. It was not used as the final gate;
the complete verifier was rerun after the visual spacing correction.

Browser recheck boundary: the final all-page invocation exited 1 after one
Robotics P58 mobile request exceeded its unchanged three-second deadline. It
retained 579 initial passes. Three isolated desktop/mobile repetitions on the
same image passed all six checks; the reconciled 580 identities retain the
original failed row and links to every recheck. This is not an initial clean
sweep or concurrent-capacity certification; the timeout cause is not proven.
