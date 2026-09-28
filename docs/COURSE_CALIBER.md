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

## Current disposition (2026-09-28)

| Course | Native interactive lessons | Required follow-up |
| --- | ---: | --- |
| DSP/Radar | 84 | #441: aggregate competency mapping and cumulative assessment after completed item repairs |
| Controls/GNC | 68 | 22 affected lessons: cumulative capstones plus unsupported prerequisite mechanisms |
| Robotics/Autonomy | 69 | 27 affected lessons: replay/recovery plus unsupported geometry, dynamics and perception mechanisms |
| Vehicle Dynamics | 67 | Repair P61–P67 dimensional/performance/cumulative defects, including hardcoded P66/P67 verdicts |

All four aggregate numerical, curriculum and capstone statuses remain blocked
pending the named reassessments. Prior maps, references and tests are retained;
the newly demonstrated defects override earlier passed labels. Learner
validation is `not_run` for every course. Browser/container acceptance is a
separate delivery check and cannot promote educational maturity.

See [the per-lesson quality board](COURSE_QUALITY.md) for the initial twelve-lesson
semantic revision group, exact findings and delivery evidence. Nine other
pinned repositories remain source-only. No MATLAB runtime, physical hardware,
measured vehicle/track, representative learner or production claim is made.

The wider direct review records 56 affected lessons, including 44 outside the
initial twelve-lesson repair. Finishing that group alone cannot close Controls
or Robotics aggregate maturity. See the per-lesson additional finding register.
