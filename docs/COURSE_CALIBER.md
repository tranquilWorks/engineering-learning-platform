# Course-caliber gate

The platform now reports course implementation and educational maturity as
different facts. A source-item, platform-module, authored, interactive, or
`P##` count is implementation inventory only. Even `84/84` or `24/24` cannot
establish curriculum completeness, numerical fidelity, integrated capstones,
or learner outcomes.

The authoritative machine-readable projection is
[`course-caliber-status.yaml`](course-caliber-status.yaml). It implements
Portfolio Control standard `ELP-COURSE-CALIBER-1` with the navigation/geometry revision contract at merged control
revision `15f2c1537b2be9710143d03ffbc182574de51376`. DSP retains its separate
aggregate evidence from control revision `7b2e3c1e425b196b400856a714f699f2e225a83a`.

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

## Current disposition (2026-09-29)

| Course | Native interactive lessons | Required follow-up |
| --- | ---: | --- |
| DSP/Radar | 84 | Authored/software aggregate review passed: 84 checkpoints, ten cumulative portfolios and 417 independent comparisons; learner validation not_run |
| Controls/GNC | 68 | Zero listed findings; 22 lessons have scoped repairs; aggregate reassessment remains pending |
| Robotics/Autonomy | 69 | 20 remaining affected lessons; P25–P29 and two capstones have scoped repairs |
| Vehicle Dynamics | 67 | 16 remaining affected lessons: P01–P16 mixed-unit charts; P61–P67 have scoped numerical/physical repairs |

Controls, Robotics and Vehicle aggregate numerical, curriculum and capstone
statuses remain blocked. DSP passes its separate authored/synthetic reassessment. Prior maps, references and tests are retained;
the newly demonstrated defects override earlier passed labels. Learner
validation is `not_run` for every course. Browser/container acceptance is a
separate delivery check and cannot promote educational maturity.

See [the per-lesson quality board](COURSE_QUALITY.md) for the initial twelve-lesson
semantic revision group, exact findings and delivery evidence. Nine other
pinned repositories remain source-only. No MATLAB runtime, physical hardware,
measured vehicle/track, representative learner or production claim is made.

The wider direct review records 72 affected lessons, including 60 outside the
initial twelve-lesson repair. Finishing that group alone cannot close Controls,
Robotics or Vehicle aggregate maturity. See the per-lesson additional finding register.

The separate DSP aggregate review closes its declared authored curriculum and
synthetic numerical/pulsed-capstone scope. Controls, Robotics and Vehicle remain
blocked: 36 named findings remain in Robotics/Vehicle, and Controls requires a separate aggregate reassessment despite zero listed findings. No course has representative-learner validation.
See course-caliber-status.yaml and the exact aggregate evidence.


## Robotics dynamics scope — 2026-09-29

Control PR569 authorized Robotics P30-P41. These twelve scoped repairs add real mechanisms, independent calculations and embedded formative checkpoints. Eight named Robotics findings remain (P42-P48/P52), alongside sixteen Vehicle findings. All non-DSP aggregate numerical, curriculum and capstone reviews remain blocked. Completing the named register is not aggregate acceptance. The active batch evidence records the required delivery/gate status.

The Robotics dynamics batch completed full delivery and mandatory sequential gates. Its verified development preview is port 8774; exact image, input hashes, results and remaining acceptance boundaries are in `docs/course-quality/robotics-dynamics-verification-summary.json`. This scoped result does not promote an aggregate course stage.
