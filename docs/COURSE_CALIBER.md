# Course-caliber gate

The platform now reports course implementation and educational maturity as
different facts. A source-item, platform-module, authored, interactive, or
`P##` count is implementation inventory only. Even `84/84` or `24/24` cannot
establish curriculum completeness, numerical fidelity, integrated capstones,
or learner outcomes.

The authoritative machine-readable projection is
[`course-caliber-status.yaml`](course-caliber-status.yaml). It implements
Portfolio Control standard `ELP-COURSE-CALIBER-1` at merged control revision
`0038f6ed725ae2fc7b3eb6647e9621a2ad23db34`.

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
| Robotics and Autonomy | 24 / 24 / 24 | `numerically_verified` | #440: fill competency gaps and add a traced cumulative capstone |

No reviewed course is marked `curriculum_covered: passed` at the Controls/GNC
remediation baseline `1506591946ec8e96fe3201e8893b8ad851a1685a`. Issue #438
has repaired P01-P24 fidelity and independent software evidence. Issues #439,
#440, and #441 remain separately owned expansion or remediation work.

Vehicle Dynamics remains queued and unimplemented. It may proceed only after
this gate is projected, its reviewed competency map is valid, replayable GR86
CAN/BLE fixtures have provenance, and a separate coherent batch of at most ten
lessons is authorized.

This projection does not claim MATLAB runtime comparison, browser or
accessibility acceptance, learner effectiveness, physical hardware/HIL,
bench, field, release, deployment, credentials/settings, or production use.
