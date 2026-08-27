# DSP/Radar conversion authoring contract

This directory is the platform-owned Python learner course derived from the
read-only canonical source repository
`tranquilWorks/dsp-radar_learning@5d73667a486df4a7b6c581e4c9406e810ed4f0f6`.
The source repository remains the subject-matter and MATLAB reference. This
directory owns only the reviewed Engineering Learning Platform representation.

The conversion sequence is fixed:

`ELP-DSP-00 -> ELP-DSP-P01 -> ... -> ELP-DSP-P84 -> ELP-DSP-G-PYTHON`

## Source identity and precedence

The following committed artifacts are the conversion authority:

- `source-map.yaml` fixes the source repository, commit, tree, curriculum
  digest, ordered P01-P84 identity, and hashes of all 420 canonical inputs.
- `conversion-manifest.yaml` fixes each source item, target folder, title,
  guiding question, phase, and successor batch.
- `coverage.yaml` is the only mutable aggregate conversion ledger.
- `conversion.schema.json` is the closed evidence contract for one completed
  target module.

Within one mapped source item, use the inputs in this order:

1. `README.md` fixes the experiment, learning goal, and completion condition.
2. `lesson.md` fixes the concept explanation, physical model, equations,
   limiting cases, and common interpretation mistakes.
3. `walkthrough.md` fixes the learner sequence, expected observations,
   parameter sweeps, broken case, and recovery.
4. `checks.md` fixes focused observation, prediction, interpretation, and
   teach-back checks.
5. `experiment.m` fixes constants, deterministic seed/data, operations, plot
   order and labels, numerical assertions, and resource guards.

Do not silently choose between conflicting source inputs. Stop the item batch,
record the exact conflict, and request a reviewed source-pin or conversion
decision. Never repair, annotate, generate into, or commit under the canonical
source submodule from a platform batch.

## Stable identity mapping

- Canonical source identity remains uppercase `P01` through `P84`.
- Native ELP module identity is the exact `target_module_id`, which is also
  the lowercase target-folder basename, for example
  `01-build-a-sinusoid-and-a-complex-phasor`.
- Native module number is the corresponding integer, 1 through 84.
- The exact source title and guiding question are copied into the native
  manifest and learner lesson.
- A module lives only at the `target_folder` recorded in
  `conversion-manifest.yaml`.
- A conversion record lives beside the module as `conversion.yaml` and must
  validate against `conversion.schema.json`.

The source map, `course.yaml`, `conversion.schema.json`, and the stable
fields in the conversion manifest never change during a P## item batch. A
different source commit, tree, folder, title, question, phase, file hash, native
course identity, or evidence contract requires a new pin/reconciliation batch.

## One-item batch boundary

An `ELP-DSP-P##` batch may:

- create exactly its mapped target module directory;
- add its `module.yaml`, `lesson.md`, self-contained `experiment.py`, and
  `conversion.yaml`;
- add item-owned deterministic fixtures or tests explicitly named by that
  batch;
- change exactly the matching coverage entry from `pending` to `converted`;
- update the coverage summary by one pending decrement and one converted
  increment; and
- add its exact evidence and authorized current-state documentation.

It may not:

- edit the source submodule or another target module;
- change the source map or stable conversion-manifest fields;
- create bulk shells, TODO pages, empty manifests, copied MATLAB files, or
  placeholder modules;
- mark a blocked, absent, non-executing, or partially evidenced item converted;
- extend generic API, React, schema, runtime, dependency, workflow, deployment,
  or security behavior without a separate reviewed platform contract; or
- merge more than one source item under one P## identity.

Run batches strictly in numeric order. The legal converted transition from a
coverage ledger at step N to N+1 changes only item N+1 and the corresponding
summary counts. A reviewed batch may instead change the earliest pending item
to `blocked` only when it adds a non-empty blocker reason and retained
evidence, increments `blocked`, and decrements `pending`. A blocked item
stops the ordered lane; it does not authorize skipping forward or relabeling a
placeholder as converted.

## Native learner module

Every converted module must be a complete vertical learner slice:

1. Short concept and guiding question.
2. A beginner-focused physical mental model.
3. The signal-flow or processing sequence.
4. Equations with plain-language meaning before a toolbox shortcut.
5. One concrete prediction.
6. Labeled controls with units where applicable.
7. Immediate metrics, plots, tables, and explanations.
8. At least two useful one-variable parameter sweeps.
9. One intentionally broken case that demonstrates a real interpretation or
   processing failure.
10. A named recovery path that returns to a verified baseline.
11. Expected observations and common interpretation mistakes.
12. A concise completion and teach-back checklist.

The native `module.yaml` uses schema version 1 and the generic platform
vocabulary. DSP and radar calculations stay in the course-owned
`experiment.py`; no subject-specific branch belongs in `apps/api`,
`apps/web`, or `packages/lesson-schema`.

Every plot must have a useful title, axis labels, and units where applicable.
Every plotted transition must have adjacent interpretation text. Controls must
be keyboard accessible through the generic renderer, visibly labeled, bounded,
and limited to the smallest set that clarifies the concept.

## Python runtime rules

Each source experiment is independently reimplemented as trusted, bounded
Python using the standard library and checked-in platform dependencies such as
NumPy, SciPy, and pandas. Return Plotly-compatible figure JSON; do not add
Matplotlib or a Plotly Python dependency.

The entrypoint must:

- be self-contained in the declared `experiment.py` because the current
  platform digest binds the direct entrypoint, not undeclared helper imports;
- accept exactly one parameter mapping and return the platform result envelope;
- use a fixed, recorded random seed whenever randomness is present;
- reject non-finite, out-of-range, excessive, or inconsistent parameters before
  allocation;
- declare a timeout, maximum sample count, and maximum serialized output size
  in `conversion.yaml`;
- keep its default run fast enough for catalog reload, which executes every
  Python module once before promotion;
- generate finite, deterministically serializable values only;
- provide stable result keys for every declared plot, table, metric, and
  explanation; and
- avoid `eval`, shell execution, subprocesses, dynamic installation, network
  access, learner code execution, and writable course state.

The Python implementation should reproduce the source experiment's conceptual
and numerical behavior, not translate MATLAB syntax line by line. Preserve
equations, constants, sample conventions, transforms, normalizations, axes,
plot sequence, assertions, and limiting cases explicitly.

## Required Python/source equivalence

`conversion.yaml.python_source_equivalence` is mandatory and its status is
always `passed` for a converted item. It cannot be absent, skipped, waived, or
replaced by screenshots, prose, static source inspection, a successful build,
or a MATLAB `not_run` result.

Retain at least one named equivalence case and include:

- exact source input hashes and source-map digest;
- deterministic inputs and seed;
- retained expected and actual numeric/vector result files with SHA-256
  identities;
- units;
- explicit absolute and relative tolerances;
- measured maximum absolute and relative error;
- the exact verification command; and
- a passing result for every case.

Case names and input names are unique. Measured absolute and relative error
must each be no greater than its declared tolerance. Image files and screenshots
cannot serve as the expected or actual numeric result.

`target.content_digest` and
`coverage.yaml.items[].target_content_digest` are the exact
`CourseCatalog` module content digest for the accepted target bytes. The
conversion record itself is deliberately outside that digest, so recording the
digest is not self-referential. Its listed target files still carry their own
SHA-256 identities.

Expected vectors may be independently derived from the source equations and
retained constants. Do not claim MATLAB execution merely because the expected
values agree with the MATLAB source text. If a source behavior cannot be
reproduced within the current generic contract or installed Python
dependencies, stop and materialize a reviewed decision instead of weakening
the case.

## Optional MATLAB runtime parity

`matlab_runtime_parity.status` is exactly one of:

- `passed`: actual MATLAB ran; record runtime, version, toolboxes, command,
  inputs, tolerances, outputs, and retained evidence.
- `failed`: actual MATLAB ran but did not meet the comparison; record runtime,
  version, toolboxes, exact command, reason, and retained numeric/log evidence.
- `not_run`: MATLAB did not run; record a non-empty reason.

`not_run` and `failed` never render or count as passed. A screenshot,
source file, source assertion, Python fixture, or hosted CI job is not evidence
that MATLAB executed.

The final Python course gate does not require MATLAB availability. It does
require every module's MATLAB status to be explicit and every Python/source
equivalence case to pass.

Every conversion record uses claim profile `elp-dsp-item-software-v1`.
Browser and accessibility review may be passed or failed only with a summary
and retained evidence; otherwise they are `not_run` with a reason. Learner
effectiveness is always `not_run` for an item conversion because repository
software verification is not a learner study.

## Coverage and visibility

`coverage.yaml` distinguishes inventory from learner readiness:

- `pending`: mapped, but no complete target learner module exists.
- `converted`: complete native module, Python runtime, source-equivalence
  record, focused tests, deterministic platform validation, and exact item
  evidence passed.
- `blocked`: an explicit reviewed blocker prevents the ordered conversion.

`placeholder` is always zero. The catalog-visible zero-module course created
by ELP-DSP-00 is framework state, not a completed lesson. A learner module is
visible only when its real `module.yaml` exists, and visibility alone does not
prove Python execution, numerical equivalence, browser review, accessibility,
or pedagogy.

## Verification and evidence

Each P## batch must retain:

- exact target baseline and candidate commit;
- exact source repository, commit, tree, source-map digest, item identity, and
  five source file hashes;
- target file identities and content digest;
- deterministic default and bounded-control execution;
- result-reference, label, unit, finite-value, serialization, and resource
  checks;
- at least two sweep checks, broken-case and recovery checks, common mistakes,
  and completion checks;
- named Python/source-equivalence results with tolerances;
- explicit MATLAB status;
- focused tests, course validation, contract, quick, full, diff, and exact-head
  hosted CI results; and
- changed/preserved invariants, rollback, residual risks, and every unperformed
  validation class.

Use precise claim vocabulary:

- `catalog-visible`: the API/UI can discover the committed module.
- `Python-verified`: its bounded native Python tests and deterministic
  platform execution passed.
- `source-equivalent`: every retained Python/source case passed its stated
  tolerances.
- `MATLAB-compared`: actual MATLAB evidence says `passed`.
- `browser-reviewed` and `accessibility-reviewed`: the named manual checks
  were actually performed.
- `learner-reviewed`: the named learner/pedagogy review was actually
  performed.

Do not collapse those states into “done” or “polished.” The aggregate
`ELP-DSP-G-PYTHON` gate is the first point allowed to claim a complete
84-module professional Python course, and only after it verifies no pending,
blocked, or placeholder items.

## Rollback and escalation

Before a successor depends on a new module, rollback is the reviewed revert of
that one P## target commit plus the exact inverse coverage transition. The
source pin and source repository remain unchanged.

After successors depend on a module, do not delete or rewrite history
piecemeal. Stop and create a coordinated forward-fix or ordered revert
contract.

Escalate instead of improvising when:

- source identity or hashes drift;
- source inputs conflict;
- the current generic renderer/runtime cannot express the lesson;
- a new dependency, helper-loading rule, schema field, or shared component is
  required;
- deterministic equivalence cannot pass honestly;
- runtime bounds cannot keep default catalog validation safe;
- more than one item would need to change;
- the source would need a write; or
- a claim would require MATLAB, browser/accessibility, learner, physical,
  HIL/HWIL, RF, real-time, release, deployment, or production evidence that was
  not actually produced.
