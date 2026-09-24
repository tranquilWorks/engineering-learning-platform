# Course-caliber gate

The platform now reports course implementation and educational maturity as
different facts. A source-item, platform-module, authored, interactive, or
`P##` count is implementation inventory only. Even `84/84` or `24/24` cannot
establish curriculum completeness, numerical fidelity, integrated capstones,
or learner outcomes.

The authoritative machine-readable projection is
[`course-caliber-status.yaml`](course-caliber-status.yaml). It implements
Portfolio Control standard `ELP-COURSE-CALIBER-1` at merged Vehicle Dynamics
P17-P24 authorization revision `16699cf63ab5dc85413acd4eacf44e9b914fe68d`.

## Six separately evidenced stages

1. `source_authored` — canonical goals, prerequisites, explanations,
   exercises, and provenance are authored rather than placeholders.
2. `platform_converted` — mapped lessons and bounded executable artifacts are
   complete and discoverable on the platform.
3. `numerically_verified` — course-specific computations pass independently
   originated references with units, tolerances, limits, and failure behavior.
4. `curriculum_covered` — a reviewed competency map proves foundations,
   breadth, sequencing, assessment, exclusions, and handoffs.
5. `capstone_integrated` — cumulative work integrates multiple mapped
   competencies and is independently assessed.
6. `learner_validated` — representative learners meet predeclared learning,
   usability, and accessibility criteria.

Passing an earlier stage never implies a later stage. Each course review
records separate evidence and limitations for every stage.

## Nine review dimensions

Every review covers foundations/prerequisites, breadth/sequencing,
derivation/physical meaning, unique executable fidelity,
sweeps/limits/failure/recovery, independent evidence, formative and cumulative
assessment, capstones, and exclusions/cross-course handoffs.

The semantic anti-template review compares unrelated competencies across their
governing relations, state, controls, transformations, outputs, failure modes,
and reference methods. Shared helpers are acceptable; one generic experiment
with renamed labels is not evidence of course-specific fidelity.

## Authorization and evidence rules

Before any new course conversion, a reviewed competency-to-module matrix must
validate against the control-plane `course-competency-map` schema. The matrix,
not a portfolio quota, determines the lesson count. Each implementation batch
must be the smallest coherent prerequisite or integration unit and may add at
most ten lessons.

Evidence labeled independent must record its origin and formulation. It cannot
import the production entrypoint, derive values from production output, or
perturb production output. Those artifacts may be useful regression fixtures,
but they are not independent correctness oracles.

## Baseline disposition

| Course | Inventory | Highest unblocked stage | Required follow-up |
| --- | ---: | --- | --- |
| DSP/Radar | 84 source / 84 platform / 84 interactive | `platform_converted` | #441: replace the P02-P84 generic execution structure and independently reverify it |
| Controls/GNC | 24 / 24 / 24 | `numerically_verified` | #439: expand against the reviewed competency map and add cumulative integration |
| Robotics and Autonomy | 24 source / 69 platform / 69 interactive | `capstone_integrated` | Maintain the reviewed map; learner/accessibility validation remains not run |
| Vehicle Dynamics | 24 source / 43 platform / 43 interactive | P01-P43 numerically verified | #467: authorize P44-P52 propulsion depth against the merged chassis-batch baseline |

Controls/GNC and Robotics/Autonomy are now marked `curriculum_covered: passed`
and `capstone_integrated: passed` from their reviewed maps and requirements-traced
software capstones. Those outcomes do not imply `learner_validated`, which remains
`not_run`. DSP/Radar remediation remains separately owned by issue #441.

Vehicle Dynamics preparation, the three source-bound arcs, and the first two
competency-derived tire- and chassis-depth arcs are complete.
The reviewed 67-module map, exact source ledger, and deterministic synthetic
GR86 CAN/BLE fixtures are installed. P01-P24 are deterministic software-only
lessons with independent scalar references; P25-P33 add independently evidenced
advanced tire models, while P34-P43 add dynamic handling, nonlinear stability,
load-transfer, ride-mode, damper, suspension, and anti-geometry models. P20 does
not use a real drive and P24 is not physical GR86 validation. P44-P67 remain
separately gated.

This projection does not claim MATLAB runtime comparison, browser or
accessibility acceptance, learner effectiveness, physical hardware/HIL,
bench, field, release, deployment, credentials/settings, or production use.
